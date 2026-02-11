import pickle
from faqbot.legacy.faq import COMMANDS


def save_commands(COMMANDS):
    pickle.dump(COMMANDS, open("faq.pkl", "wb"))


def load_commands():
    return pickle.load(open("faq.pkl", "rb"))


def pickle_faq():
    pickle.dump(COMMANDS, open("faq.pkl", "wb"))
