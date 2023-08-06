"""Slurm job class for handling Slurm jobs using pycondor.job.Job.
"""

import subprocess
import os

import pycondor.job
import pycondor.utils


class SlurmJob(pycondor.job.Job):
    """A class for handling Slurm job.
    """
    def __init__(self,
                 name,
                 executable,
                 error=None,
                 output=None,
                 submit=None,
                 nodes=None,
                 ntasks_per_node=None,
                 cpus_per_task=None,
                 mem_per_node=None,
                 extra_sbatch_options=None,
                 extra_srun_options=['ntasks=1', 'exclusive'],
                 extra_lines=None,
                 modules=None,
                 slurm=None,
                 arguments=None,
                 verbose=0):
        """Constructor.

        Parameters
        ----------
        name: str
            Name of the job.
        executable: str
            Path of the executable for the job.
        error: str, optional
            Directory of error files.
        output: str, optional
            Directory of output files.
        submit: str, optional
            Directory of submit files.
        nodes: str, optional
            <minnodes[-maxnodes]>
            Request that a minimum of minnodes nodes be allocated to
            this job.
            A maximum node count may also be specified with maxnodes.
            If only one number is specified, this
            is used as both the minimum and maximum node count.
        ntasks_per_node: str, optional
            <ntasks>
            Request that ntasks be invoked on each node.
        cpus_per_task: str, optional
            <ncpus>
            Request that ncpus be allocated per process.
        mem_per_node: str, optional
            <size[units]>
            Specify the real memory required per node.
        extra_sbatch_options: array-like str, optionl
            An array of extra options to append after '#SBATCH '.
        extra_srun_option: array-like str, optional
            An array of extra options to append after 'srun'.
        extra_lines: array-like str, optional
            An array of extra lines to add before srun.
        modules: array-like str, optional
            An array of modules to append after 'module load '.
        slurm: Slurm, optional
            If specified, SlurmJob will be added to Slurm.
        arguments: str or iterable, optional
            Arguments to initialize the job list.
        verbose: int, optional
            Level of logging verbosity option are 0-warning, 1-info,
            2-debugging (default is 0).
        """
        super().__init__(name=name, executable=executable, error=error,
                         output=output, submit=submit, dag=slurm,
                         arguments=arguments, verbose=verbose)
        self._slurm_nodes = nodes
        self._slurm_ntasks_per_node = ntasks_per_node
        self._slurm_cpus_per_task = cpus_per_task
        self._slurm_mem_per_node = mem_per_node
        self._slurm_extra_sbatch_options = extra_sbatch_options
        self._slurm_extra_srun_options = extra_srun_options
        self._slurm_extra_lines = extra_lines
        self._slurm_modules = modules

    def __repr__(self):
        nondefaults = ''
        default_attr = ['name', 'executable', 'logger']
        for attr in sorted(vars(self)):
            if getattr(self, attr) and attr not in default_attr:
                nondefaults += ', {}={}'.format(attr, getattr(self, attr))
        output = 'SlurmJob(name={}, executable={}{})'.format(
            self.name, os.path.basename(self.executable), nondefaults)
        return output

    def build(self, makedirs=True, fancyname=True):
        """Build and save the submit file for Job.

        Parameters
        ----------
        makedirs: bool, optional
            Create job directories if not exist.
        fancyname: bool, optional
            Append the name with date and unique id.

        Returns
        -------
        self: object
            Self object.
        """
        self.logger.info(
            "Building submission file for Job {}...".format(self.name))
        self._make_submit_script(makedirs, fancyname)
        self._built = True
        self.logger.info(
            "Submission file for {} successfully built!".format(self.name))
        return self

    @pycondor.utils.requires_command("sbatch")
    def submit_job(self, submit_options=None):
        """Submit Job to Slurm.

        Parameters
        ----------
        submit_options: str, optional
            Submit options appends after sbatch.

        Returns
        -------
        self: object
            Self object.
        """
        if not self._built:
            raise ValueError("build() must be called before submit(). ")
        if len(self.parents) != 0:
            raise ValueError("Attempting to submit a Job with parents. "
                             "Interjob relationship requires Slurm.")
        if len(self.children) != 0:
            raise ValueError("Attempting to submit a Job with children. "
                             "Interjob relationship requires Slurm.")
        command = "sbatch"
        if submit_options is not None:
            command += " {}".format(submit_options)
        command += " {}".format(self.submit_file)

        proc = subprocess.Popen(
            pycondor.utils.split_command_string(command),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        out, err = proc.communicate()
        print(pycondor.utils.decode_string(out))
        return self

    @pycondor.utils.requires_command("sbatch")
    def build_submit(self, makedirs=True, fancyname=True, submit_options=None):
        """Build and submit sequentially.

        Parameters
        ----------
        makedirs: bool, optional
            Create directories if not exist.
        fancyname: bool, optional
            Append date of unique id to submit.
        submit_options: str, optional
            Options to be passed to 'sbatch'.

        Returns
        -------
        self: object
            Self object.
        """
        self.build(makedirs, fancyname)
        self.submit_job(submit_options=submit_options)
        return self

    def _make_submit_script(self, makedirs=True, fancyname=True):
        """Make the submit script.

        Parameters
        ----------
        makedirs: bool, optional
            Create job directories if not exist.
        fancyname: bool, optional
            Append the name with date and unique id.
        """
        # Check directories.
        for directory in [self.submit, self.output, self.error]:
            if directory is not None:
                pycondor.utils.checkdir(os.path.join(directory, ""), makedirs)
        name = self._get_fancyname() if fancyname else self.name

        submit_file = (
            os.path.join(self.submit, "{}.submit".format(name))
            if self.submit is not None
            else "{}.submit".format(name)
        )
        output_file = (
            os.path.join(self.output, "{}.output".format(name))
            if self.output is not None
            else "{}.output".format(name)
        )
        error_file = (
            os.path.join(self.error, "{}.error".format(name))
            if self.error is not None
            else "{}.error".format(name)
        )
        self.submit_file = submit_file
        self.output_file = output_file
        self.error_file = error_file
        self.submit_name = name

        with open(self.submit_file, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("#SBATCH --job-name={}\n".format(name))
            f.write("#SBATCH --output={}\n".format(output_file))
            f.write("#SBATCH --error={}\n".format(error_file))
            if self._slurm_nodes is not None:
                f.write("#SBATCH --nodes={}\n".format(self._slurm_nodes))
            if self._slurm_ntasks_per_node is not None:
                f.write("#SBATCH --ntasks-per-node={}\n"
                        "".format(self._slurm_ntasks_per_node))
            if self._slurm_cpus_per_task is not None:
                f.write("#SBATCH --cpus-per-task={}\n"
                        "".format(self._slurm_cpus_per_task))
            if self._slurm_mem_per_node is not None:
                f.write("#SBATCH --mem={}\n".format(self._slurm_mem_per_node))
            if self._slurm_extra_sbatch_options is not None:
                for option in self._slurm_extra_sbatch_options:
                    f.write("#SBATCH --{}\n".format(option))
            f.write("\n")
            if self._slurm_extra_lines is not None:
                for extra_line in self._slurm_extra_lines:
                    f.write("{}\n".format(extra_line))
                f.write("\n")
            if self._slurm_modules is not None:
                for module in self._slurm_modules:
                    f.write("module load {}\n".format(module))
                f.write("\n")
            base_arg = "srun"
            if self._slurm_extra_srun_options:
                for option in self._slurm_extra_srun_options:
                    base_arg += " --{}".format(option)
            for arg in self.args:
                f.write("{} {} {} &\n"
                        "".format(base_arg, self.executable, arg.arg))
            f.write("wait\n")
