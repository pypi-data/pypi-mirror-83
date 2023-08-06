# -*- coding: utf-8 -*-
"""Gaia Auth class file."""


class Auth:
    """Gaia Auth class."""

    def __init__(self, gaia):
        """Initialize a class instance."""
        self.gaia = gaia

    def ad_ldap(self):
        """Return an authorized AD instance."""
        from bits.ldap.ad import AD
        settings = self.gaia.get_settings("ad_ldap")
        return AD(
            uri=settings.get("uri"),
            bind_dn=settings.get("bind_dn"),
            bind_pw=self.gaia.get_secret(settings.get("bind_pw_name")),
            base_dn=settings.get("base_dn"),
            server_type="ad",
            verbose=self.gaia.verbose,
        )

    def bitsdb_mongo(self):
        """Return an authorized Mongo instance for BITSdb."""
        from bits.mongo import Mongo
        settings = self.gaia.get_settings("bitsdb_mongo")
        db = settings.get("db")
        host = settings.get("host")
        username = settings.get("username")
        password = self.gaia.get_secret(settings.get("password_name"))
        return Mongo(
            uri=f"mongodb://{username}:{password}@{host}/{db}",
            db=db,
            verbose=self.gaia.verbose,
        )

    def gaia_sftp(self):
        """Return an authorized SFTP instance for gaia."""
        from bits.sftp import SFTP
        settings = self.gaia.get_settings("gaia_ssh")
        return SFTP(
            host=settings.get("host"),
            path=settings.get("path"),
            username=settings.get("username"),
            key=self.gaia.get_secret(settings.get("key_name")),
        )

    def google(self, scopes):
        """Return an authorized Google instance for gaia."""
        from bits.google import Google
        return Google(scopes=scopes)

    def people_mysql(self):
        """Return an authorized MySQL instance for People."""
        from bits.mysql import MySQL
        settings = self.gaia.get_settings("people_mysql")
        return MySQL(
            server=settings.get("server"),
            port=settings.get("port"),
            user=settings.get("user"),
            password=self.gaia.get_secret(settings.get("password_name")),
            db=settings.get("db"),
            verbose=self.gaia.verbose,
        )

    def sap_mssql(self):
        """Return an authorized MSSQL instance for SAP datawarehouse."""
        from bits.mssql import MSSQL
        settings = self.gaia.get_settings("sap_mssql")
        server = settings.get("server")
        port = settings.get("port")
        return MSSQL(
            server=f"{server}:{port}",
            user=settings.get("user"),
            password=self.gaia.get_secret(settings.get("password_name")),
            database=settings.get("db"),
            verbose=self.gaia.verbose,
        )

    def space_mysql(self):
        """Return an authorized MySQL instance for Space."""
        from bits.mysql import MySQL
        settings = self.gaia.get_settings("space_mysql")
        return MySQL(
            server=settings.get("server"),
            port=settings.get("port"),
            user=settings.get("user"),
            password=self.gaia.get_secret(settings.get("password_name")),
            db=settings.get("db"),
            verbose=self.gaia.verbose,
        )
