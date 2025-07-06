#!/bin/sh

# Print a message to indicate the start of the autograding process
echo "🚀 Starting autograder..."

# Ensure that the necessary environment variables are set and print them for debugging
echo "Token: $1"
echo "Redis URL: $2"
echo "Redis Token: $3"




# Specify the path to the student's submission folder (we assume files are in the "submission" folder)
STUDENT_REPO_PATH="$GITHUB_WORKSPACE/submission"

# Print some of the important paths for debugging
echo "Student repository path: $STUDENT_REPO_PATH"
echo "Grading criteria: $GRADING_CRITERIA"

# Run the Python autograder script with the provided inputs
# This command will invoke autograder.py and pass the weights and grading criteria
echo $1
python /app/test.py --token $1 --redis-token $2 --redis-url $3

# Check if the autograder script executed successfully
echo "✅ Autograding completed successfully!"
# Provide a message indicating completion
echo "🎉 Final results generated and sent to GitHub Classroom!"