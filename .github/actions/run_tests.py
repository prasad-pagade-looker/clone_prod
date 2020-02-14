from looker_sdk import client, models
import sys

sdk = client.setup()

def main():
    broken_content_prod = sdk.content_validation().content_with_errors
    
    """Enter dev mode """
    sdk.update_session(models.WriteApiSession(workspace_id='dev'))
    
    """ Check out this branch """
    branch = sys.argv[1].replace("refs/heads/","")
    resp = sdk.update_git_branch(project_id=sys.argv[2], body=models.WriteGitBranch(name=branch))
    broken_content_dev = sdk.content_validation().content_with_errors

    # Assert no new errors introduced in dev branch
    assert len(broken_content_dev) - len(broken_content_prod) <= 0, """
        Uh oh. you just introduced a new content error!"""

    tests = sdk.all_lookml_tests(project_id=sys.argv[2])
    for test in tests:
        resp = sdk.run_lookml_test(project_id=sys.argv[2], test=test.name, model=test.model_name)
        assert resp[0].assertions_failed == 0, resp[0].errors

main()
