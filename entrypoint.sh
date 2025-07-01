#!/bin/sh

# Print a message to indicate the start of the autograding process
echo "🚀 Starting autograder..."

# Ensure that the necessary environment variables are set and print them for debugging
echo "HTML Weight: $1"
echo "CSS Weight: $2"
echo "JS Weight: $3"
echo "Timeout: $4"
echo "token: $5"



# Specify the path to the student's submission folder (we assume files are in the "submission" folder)
STUDENT_REPO_PATH="$GITHUB_WORKSPACE/submission"

# Print some of the important paths for debugging
echo "Student repository path: $STUDENT_REPO_PATH"
echo "Grading criteria: $GRADING_CRITERIA"

# Run the Python autograder script with the provided inputs
# This command will invoke autograder.py and pass the weights and grading criteria
echo $1
python /app/test.py --token $1 --redis-url "AWeVAAIjcDFhY2ZkOGUzYWUxMTg0NTA0YWMwM2I3ZDFiYTliNWQ3MnAxMA" --redis-token "https://grown-opossum-26517.upstash.io"

# Check if the autograder script executed successfully
echo "✅ Autograding completed successfully!"
# Provide a message indicating completion
echo "🎉 Final results generated and sent to GitHub Classroom!"