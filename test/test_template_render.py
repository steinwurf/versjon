import versjon.template_render


def test_template_render(datarecorder):

    # Taken from test/recordings/context.json
    context = {
        "current": "1.1.0",
        "docs_path": {
            "1.0.0": "build_1.0.0",
            "1.1.0": "build_1.1.0",
            "2.0.0": "build_2.0.0",
            "abc": "build_abc",
            "master": "build_master"
        },
        "docs_root": '../',
        "is_semver": True,
        "other": [
            "master",
            "abc"
        ],
        "semver": [
            "2.0.0",
            "1.1.0",
            "1.0.0"
        ],
        "stable": "2.0.0"
    }

    template_render = versjon.template_render.TemplateRender(user_path=None)

    result = template_render.render(
        template_file='footer.html', **context)

    datarecorder.record_data(
        data=result, recording_file='test/recordings/footer.html')
