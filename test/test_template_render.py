import versjon.template_render


def test_template_render(datarecorder):

    # Partly taken from test/recordings/general_context.json
    context = {
        "current": "1.1.0",
        "page": "path/to/old_file.html",
        "page_root": "../",
        "is_semver": True,
        "docs_path": {
            "1.0.0": "build_1.0.0",
            "1.1.0": "build_1.1.0",
            "2.0.0": "build_2.0.0",
            "abc": "build_abc",
            "master": "build_master",
        },
        "other": [
            {
                "name": "master",
                "html_files": ["path/to/new_file.html", "path/to/old_file.html"],
            },
            {"name": "abc", "html_files": []},
        ],
        "semver": [
            {"name": "2.0.0", "html_files": ["path/to/old_file.html"]},
            {"name": "1.1.0", "html_files": ["path/to/old_file.html"]},
            {"name": "1.0.0", "html_files": ["path/to/old_file.html"]},
        ],
        "stable": "2.0.0",
    }

    template_render = versjon.template_render.TemplateRender(user_path=None)

    result = template_render.render(template_file="footer.html", **context)

    datarecorder.record_data(data=result, recording_file="test/recordings/footer.html")
