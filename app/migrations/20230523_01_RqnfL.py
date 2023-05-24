"""

"""

from yoyo import step

__depends__ = {}

steps = [
    step(""" CREATE TABLE db.user (
            login VARCHAR(50),
            nome VARCHAR(100),
            email VARCHAR(50),
            senha VARCHAR(50),
            status BOOL,
            PRIMARY KEY (email)
        );
        """),
    step(
        """
        INSERT INTO db.user (login, nome, email, senha, status)
        VALUES
        ('user1', 'John Smith', 'johnsmith@example.com', 'password123', true),
        ('user2', 'Jane Doe', 'janedoe@example.com', 'abc123', true),
        ('user3', 'Michael Johnson', 'michaelj@example.com', 'pass456', true),
        ('user4', 'Sarah Williams', 'sarahw@example.com', 'secure789', false);"""
        )
]
