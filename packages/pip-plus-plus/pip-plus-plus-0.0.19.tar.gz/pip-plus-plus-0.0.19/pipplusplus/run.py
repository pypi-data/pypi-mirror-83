from view.application.web_pipper_factory import FlaskPipperFactory


def run():
    app = FlaskPipperFactory.get_pipper()
    app.run()


if __name__ == '__main__':
    run()
