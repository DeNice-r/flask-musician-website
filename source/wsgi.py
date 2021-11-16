from app import app


# Controllers
import controllers.index_controller
import controllers.about_controller
import controllers.history_controller
import controllers.album_controller
import controllers.login_controller
import controllers.error_controller


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=True)
