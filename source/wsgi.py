from app import *


# Controllers
import controllers.index_controller
import controllers.about_controller
import controllers.history_controller
import controllers.album_controller
import controllers.login_controller
import controllers.error_controller

import models.album
import models.user


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port='80', debug=False)
