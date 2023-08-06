"""Slurm class to build slurm job with pycondor.
"""

import subprocess
import os

import pycondor.dagman
import pycondor.utils


class Slurm(pycondor.dagman.Dagman):
    """Slurm object manages the workflow of a series of SlurmJobs.
    """
    def __init__(self,
                 name,
                 submit=None,
                 extra_lines=None,
                 verbose=0):
        """Constructor.

        Parameters
        ----------
        name: str
            Name of the Dagman instance.

        submit: str
            Directory to write submit files.

        extra_lines: array-like str
            Extra lines to add into the submit file.

        verbose: int
            Level of logging verbosity.
        """
        super().__init__(name=name, submit=submit, extra_lines=extra_lines,
                         verbose=verbose)

    def __repr__(self):
        nondefaults = ''
        for attr in sorted(vars(self)):
            if getattr(self, attr) and attr not in ['name', 'nodes', 'logger']:
                nondefaults += ', {}={}'.format(attr, getattr(self, attr))
        output = 'Slurm(name={}, n_nodes={}{})'.format(self.name,
                                                       len(self.nodes),
                                                       nondefaults)
        return output

    def build(self, makedirs=True, fancyname=True):
        """Build slurm submit files.

        Parameters
        ----------
        makedirs: bool, optional
            Create job directories if do not exist.

        fancyname: bool, optional
            Append the date and unique id number to error, log, output
            and submit files.
        """
        if getattr(self, '_built', False):
            self.logger.warning(
                '{} submit file has already been built. '
                'Skipping the build process...'.format(self.name))
            return self

        name = self._get_fancyname() if fancyname else self.name
        submit_file = (
            os.path.join(self.submit, "{}.submit".format(name))
            if self.submit is not None
            else "{}.submit".format(name)
        )
        output_file = (
            os.path.join(self.submit, "{}.output".format(name))
            if self.submit is not None
            else "{}.output".format(name)
        )
        error_file = (
            os.path.join(self.submit, "{}.error".format(name))
            if self.submit is not None
            else "{}.error".format(name)
        )
        self.submit_file = submit_file
        self.output_file = output_file
        self.error_file = error_file
        self.submit_name = name
        pycondor.utils.checkdir(self.submit_file, makedirs)
        with open(submit_file, "w") as f:
            f.write("#!/bin/bash\n")
            # Standard output and error.
            f.write("#SBATCH --job-name={}\n".format(name))
            f.write("#SBATCH --output={}\n".format(output_file))
            f.write("#SBATCH --error={}\n\n".format(error_file))
            # Write extra lines if any.
            if self.extra_lines is not None:
                for extra_line in self.extra_lines:
                    f.write("{}\n".format(extra_line))
                f.write("\n")
            # Write jobs.
            # Get a map from the job name to the job id.
            job_map = {self.nodes[i].name: i for i in range(len(self.nodes))}
            for i in range(len(self.nodes)):
                self.nodes[i].build(makedirs, fancyname)
                submit_str = "jid{}=($(sbatch".format(i)
                # Get parents of the job.
                parents = [job.name for job in self.nodes[i].parents]
                if len(parents) > 0:
                    submit_str += " --dependency=afterok"
                    for parent in parents:
                        submit_str += ":${{jid{}[-1]}}".format(job_map[parent])
                submit_str += " {}))".format(self.nodes[i].submit_file)
                f.write("{}\n".format(submit_str))
        self._built = True
        self.logger.info("Slurm submission file for {} successfully "
                         "built!".format(self.name))
        return self

    @pycondor.utils.requires_command("sbatch")
    def submit_slurm(self, submit_options=None):
        """Submit to slurm.

        Parameters
        ----------
        submit_options: str, optional
            Submit options appends after sbatch.
        """
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
        self.submit_slurm(submit_options=submit_options)
        return self

    def add_job(self, job):
        """Add job to Slurm.

        Parameters
        ----------
        job: SlurmJob
            SlurmJob to append to Slurm job list.
        """
        super().add_job(job)

    def visualize(self, filename=None):
        """Visualize Slurm graph.

        Parameters
        ----------
        filename: str or None, optional
            File to save graph diagram to. If ``None`` then no file is saved.
            Valid file extensions are ‘png’, ‘pdf’, ‘dot’, ‘svg’, ‘jpeg’, ‘jpg’.
        """
        super().visualize(filename)

    def add_child(self, node):
        """Override the parent method."""
        raise NotImplementedError

    def add_children(self, nodes):
        """Override the parent method."""
        raise NotImplementedError

    def add_parent(self, node):
        """Override the parent method."""
        raise NotImplementedError

    def add_parents(self, nodes):
        """Override the parent method."""
        raise NotImplementedError

    def add_subdag(self, dag):
        """Override the parent method."""
        raise NotImplementedError

    def haschildren(self):
        """Override the parent method."""
        raise NotImplementedError

    def hasparents(self):
        """Override the parent method."""
        raise NotImplementedError

    def submit_dag(self, submit_options=None):
        """Override the parent method.
        """
        raise NotImplementedError
