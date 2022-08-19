import configparser
# import logging
import os.path


class Config:
    fileName = "config.cfg"
    cfg = configparser.ConfigParser()

    websec = "Web Server Settings"
    webhost="Host Address"
    webport="Post Number"

    emailsec = "Email Host Settings"
    emailfrom = "From Address"
    emailfromname = "From Name"
    emailpassword = "Password"
    emailserver = "SMTP Server Addr"
    emailserverport = "SMTP Server Port"

    @staticmethod
    def generateConfig():
        gereateFileIfNotExist = open("config.cfg", "a")
        gereateFileIfNotExist.close()

        Config.cfg.add_section(Config.websec)
        Config.cfg.set(Config.websec, Config.webhost, "0.0.0.0")
        Config.cfg.set(Config.websec, Config.webport, "80")
        
        Config.cfg.add_section(Config.emailsec)
        Config.cfg.set(Config.emailsec, Config.emailfrom, "mail@mail.com")
        Config.cfg.set(Config.emailsec, Config.emailfromname, "Mail User")
        Config.cfg.set(Config.emailsec, Config.emailpassword, "password")
        Config.cfg.set(Config.emailsec, Config.emailserver, "mail.privateemail.com")
        Config.cfg.set(Config.emailsec, Config.emailserverport, "465")

        Config.saveConfig()
        # logging.info("Generated New Config")
    @staticmethod
    def init():
        file_exists = os.path.exists(Config.fileName)
        if not file_exists:
            # logging.warning("Config File Does NOt Exsist")
            Config.generateConfig()
            Config.loadConfig()

    @staticmethod
    def deleteConfig():
        overwriteFile = open("config.cfg", "w")
        overwriteFile.close()

    @staticmethod
    def saveConfig():
        # Save any configuration changes
        with open(Config.fileName, "w") as configfile:
            Config.cfg.write(configfile)

    @staticmethod
    def loadConfig():
       Config.cfg.read(Config.fileName)
        # logging.info("Config Paramters Loaded")

    