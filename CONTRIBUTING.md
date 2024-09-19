# Contributing to App Store and Google Play Store Submission Action

First off, thank you for considering contributing to the App Store and Google Play Store Submission Action! It's people like you that make it a great tool for everyone.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct. Please report unacceptable behavior to [INSERT EMAIL HERE].

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

- Use a clear and descriptive title for the issue to identify the problem.
- Describe the exact steps which reproduce the problem in as many details as possible.
- Provide specific examples to demonstrate the steps.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

- Use a clear and descriptive title for the issue to identify the suggestion.
- Provide a step-by-step description of the suggested enhancement in as many details as possible.
- Provide specific examples to demonstrate the steps.

### Pull Requests

Here's a quick guide on how to submit a pull request (PR):

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

### Running Tests

Before submitting a pull request, make sure to run the tests locally. This helps ensure that your changes haven't broken any existing functionality. Here's how to run the tests:

1. Make sure you have all the dependencies installed:
   ```
   pip install -r requirements.txt
   ```

2. Run the tests using the unittest module:
   ```
   python -m unittest test_app_store_submit.py
   ```

3. If you've added new functionality, please add appropriate tests in the `test_app_store_submit.py` file.

4. Ensure all tests pass before submitting your pull request.

If you encounter any issues running the tests, please check that your environment is set up correctly and that all dependencies are installed. If problems persist, feel free to open an issue describing the problem.

### Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

## Styleguides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Python Styleguide

All Python code must adhere to the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/).

### Documentation Styleguide

- Use [Markdown](https://daringfireball.net/projects/markdown/).
- Reference function names, variables, and literals in backticks.

## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help us track and manage issues and pull requests.

* `bug` - Issues for bugs in the code
* `documentation` - Issues or PRs related to documentation
* `enhancement` - Issues for new features or improvements
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed

## Questions?

Don't hesitate to contact the project maintainers if you have any questions or need further clarification on how to contribute.

Thank you for contributing to the App Store and Google Play Store Submission Action!
