from .choice_constructor import Choice


class ValidationErrorChoice(dict, Choice):
    #  Basic Errors #####
    ACCESS_DENIED = {
        "status": 101,
        "detail": "Access Denied!"
    }
    TOKEN_FORMAT_INCORRECT = {
        "status": 212,
        "detail": "Формат токена неправильный!"
    }
    NOT_FOUND = {
        "status": 404,
        "detail": "Not Found!"
    }
    TOKEN_ERROR = {
        "status": 111,
        "detail": "Ошибка токена!"
    }
    USER_TOKEN_NOT_FOUND = {
        "status": 101,
        "detail": "Given user's Token Not Found!"
    }
    USER_DATA_OR_USER_NOT_FOUND = {
        "status": 303,
        "detail": "Данные пользователя не переданы или пользователь не найден!"
    }
    NUMBER_ALREADY_EXISTS = {
        "status": 222,
        "detail": "Такой номер уже существует!"
    }
    ALREADY_UPDATED = {
        "status": 888,
        "detail": "Already updated!"
    }
    REQUIRED_FIELDS_NOT_FOUND = {
        "status": 999,
        "detail": "Some Required Fields Not Found!"
    }
    ERROR = {
        "status": 919,
        "detail": "ERROR!"
    }
    ALREADY_EXISTS = {
        "status": 424,
        "detail": "Already exists!"
    }
    ALREADY_REGISTERED = {
        "status": 525,
        "detail": "Already Registered!"
    }
    NOTIFICATION_STATUS_NOT_FOUND = {
        "status": 717,
        "detail": "Notification Status Not Found!"
    }

    TEMPORARILY_NOT_WORK = {
        "status": -1,
        "detail": "Функционал временно недоступен!"
    }

    # Auth Errors #####
    # EMAIL_EXISTS = {"status": 1, "detail": "Given 'email' already exists!"}
    PHONE_NUM_EXISTS = {"status": 3, "detail": "Такой номер уже существует!"}
    INACTIVE_USER = {"status": 4, "detail": "Пользователь деактивирован! Пожалуйста, обратитесь в поддержку!"}
    EMAIL_OR_PASSWORD_INCORRECT = {"status": 5, "detail": "Логин или пароль неверны!"}
    EMAIL_OR_PASSWORD_NOT_FOUND = {"status": 6, "detail": "ERROR: email или пароль не найден!"}
    EMAIL_OR_CODE_NOT_FOUND = {"status": 14, "detail": "ERROR: email или код не найден!"}

    # Users Errors #####
    EMAIL_NOT_FOUND = {"status": 13, "detail": "ERROR: email  не найден!"}
    USER_MUST_HAVE_ADDRESS = {
        "status": 7,
        "detail": 'ERROR: Поле "Адрес" обязательное!'
    }
    PAS1_or_PAS2_NOT_FOUND = {
        "status": 8,
        "detail": 'ERROR: "new_password1" or "new_password2" value not found!!'
    }
    PAS1_or_PAS2_NOT_EQUAL = {
        "status": 9,
        "detail": 'ERROR: "new_password1" and "new_password2" value not equal each other!!'
    }
    PASSWORD_NOT_FOUND = {
        "status": 10,
        "detail": 'ERROR: пароль не найден!'
    }
    PASSWORD_INCORRECT = {
        "status": 11,
        "detail": 'ERROR: пароль неправильный!'
    }
    EMAIL_OTP_INCORRECT = {
        "status": 12,
        "detail": 'ERROR: Ваш код неверный!'
    }
    RESEND_OTP = {
        "status": 13,
        "detail": 'ERROR: Перезапросите код на ваш email!'
    }

