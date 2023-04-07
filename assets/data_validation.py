import re


class InvalidData:
    def __init__(self, message, field):
        self.message = message
        self.field = field


def fix_name_casing(name):
    return name[0].upper() + name[1:].lower()


def validate_name(name):

    invalid = None

    if len(name) > 20:
        invalid = InvalidData(
            "Vardas arba pavardė yra per ilgi (iki 20 raidžių)", "name"
        )

    if len(name) < 3:
        invalid = InvalidData(
            "Vardas arba pavardė yra per trumpi (nuo 3 raidžių)", "name"
        )

    if not re.match("^[A-ZĄČĘĖĮŠŲŪŽa-ząčęėįšųūž]+$", name):
        invalid = InvalidData(
            "Vardas ir pavardė turi būti sudaryti tik iš raidžių (lotyniškų ir/ar lietuviškų)",
            "name",
        )

    return invalid


def validate_email(email):

    invalid = None

    if len(email) > 320:
        invalid = InvalidData(
            "El. paštą gali sudaryti daugiausiai 320 simbolių", "email"
        )

    if not re.match("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}([.]\w{2,3})?$", email):
        invalid = InvalidData("Netaisyklingas el. pašto formatas", "email")

    return invalid


def validate_password(password):

    invalid = None

    if not re.match("(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])", password):
        invalid = InvalidData(
            "Slaptažodį turi turėti bent vieną didžiąją, mažają raides ir skaičių",
            "password",
        )

    if len(password) > 64 or len(password) < 5:
        invalid = InvalidData(
            "Slaptažodį turi sudaryti nuo 5 iki 64 simbolių",
            "password",
        )

    return invalid
