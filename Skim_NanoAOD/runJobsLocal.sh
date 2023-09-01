#!/bin/bash
source sample/FilesNano_cff.sh

# Number of parallel jobs to run
num_parallel=5

# File containing the commands for each job
commands_file="condor/tmpSub/localResubmitJobs.txt"

# Read the total number of jobs from the number of lines in the commands file
total_jobs=$(wc -l < $commands_file)

# Define the function that will be executed in parallel
run_job() {
    command=$1
    job_number=$2
    echo "Running job $job_number"
    echo $command
    # Run the command for the job
    eval $command
    echo "Job $job_number completed"
}

# Loop through the total number of jobs
for ((job=1; job<=total_jobs; job+=num_parallel)); do
    # Run parallel jobs
    for ((i=0; i<num_parallel; i++)); do
        job_index=$((job + i))
        if [ $job_index -le $total_jobs ]; then
            command=$(sed -n "${job_index}p" $commands_file)  # Get the command from the file
            run_job "$command" $job_index &
        fi
    done

    # Wait for the parallel jobs to finish
    wait
done

echo "All jobs completed"

