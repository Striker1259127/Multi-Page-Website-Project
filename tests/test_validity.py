"""
Test for HTML and CSS validity
"""
from file_clerk import clerk
from webcode_tk import validator_tools as validator



def get_html_error_report(html_files: list) -> list:
    results = []
    for file in html_files:
        report = validator.get_validation_by_browser(file)
        for item in report:
            filename = clerk.get_file_name(file)
            expected = f"pass: {filename} has no HTML errors!"
            if "The document validates" in item.text:
                results.append((expected, f"pass: {filename} has no HTML errors!"))
            else:
                content = item.text.split("Error:")
                content.remove("")
                errors = [f"fail: {filename} {msg}" for msg in content]
                for error in errors:
                    message = error.split(">")
                    error = message[0]
                    error = error.replace("  ", " ")
                    results.append((error, expected))
    return results


project_path = "project/"
css_validation_results = validator.get_project_validation(project_path, "css")
html_results = []
html_files = clerk.get_all_files_of_type(project_path, "html")
html_results = validator.get_project_validation(project_path, "html")
print()


@pytest.mark.parametrize("result,expected", html_results)
def test_html_validity(result, expected):
    assert result == expected


@pytest.mark.parametrize("result", css_validation_results)
def test_css_validity(result):
    assert "pass" in result[:4]
