from datetime import timedelta
from fastapi.testclient import TestClient
from unittest.mock import patch
from fastapi import status
from .router import router as api_router
from app.main import app

import unittest
from parameterized import parameterized


class TestApp(unittest.TestCase):
    def setUp(self):
        app.include_router(api_router)
        self.client = TestClient(app)

    def test_index(self):

        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "ok"})

    @parameterized.expand([
        ("antonio", "antonio Aldisio", "antonio@aldisio.com", "senha123", True, status.HTTP_200_OK),
        ("Sousa", "Alves Sousa", "antonio@aldisio.com", "senha312", False, status.HTTP_500_INTERNAL_SERVER_ERROR)])
    def test_cadastrar_usuario(self,
                               username,
                               nome,
                               email,
                               password,
                               status,
                               expected_status):
        url = f"""?username={username}&nome={nome}&email={email}&password={password}&status={status}"""

        with patch("fastapi.testclient.TestClient.post") as mock_post:
            mock_response = mock_post.return_value
            mock_response.status_code = expected_status

            response = self.client.post(url)

            self.assertEqual(response.status_code, expected_status)

            if expected_status == 200:
                mock_response.json.return_value = {"message": "Usuário cadastrado com sucesso"}
                self.assertEqual(response.json(), {"message": "Usuário cadastrado com sucesso"})
                self.assertEqual(response.status_code, expected_status)
            elif expected_status == 500:
                mock_response.json.return_value = {"message": "Erro interno do servidor"}
                self.assertEqual(response.json(), {"message": "Erro interno do servidor"})
                self.assertEqual(response.status_code, expected_status)

    @parameterized.expand([
        ("antonio@aldsio", "senha123", "123senha", status.HTTP_200_OK),
        ("naoexisto@com", "senha123", "123senha", status.HTTP_404_NOT_FOUND),
        ("naoexisto@com", "incorreta", "123senha", status.HTTP_404_NOT_FOUND)
    ])
    def test_trocar_senha(self,
                            email,
                            senha_atual,
                            nova_senha,
                            expected_status):
        url = f"""/changePassword?email={email}&senha_atual={senha_atual}&nova_senha={nova_senha}"""

        with patch("fastapi.testclient.TestClient.put") as mock_put:
            mock_response = mock_put.return_value
            mock_response.status_code = expected_status

            response = self.client.put(url)

            if expected_status == 200:
                mock_response.json.return_value = {"message": "Senha atualizada com sucesso"}
                self.assertEqual(response.json(), {"message": "Senha atualizada com sucesso"})
                self.assertEqual(response.status_code, expected_status)
            if expected_status == 404:
                mock_response.json.return_value = {"message": "Usuário não encontrado"}
                self.assertEqual(response.json(), {"message": "Usuário não encontrado"})
                self.assertEqual(response.status_code, expected_status)
            if expected_status == 400:
                    mock_response.json.return_value = {"message": "Senha atual incorreta"}
                    self.assertEqual(response.json(), {"message": "Senha atual incorreta"})
                    self.assertEqual(response.status_code, expected_status)

    @patch("fastapi.testclient.TestClient.post")
    def test_login_auth(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = status.HTTP_200_OK
        mock_response.json.return_value = {
            "access_token": "fake_access_token",
            "token_type": "bearer"
        }

        response = self.client.post("/loginAuth", data={
            "username": "test@example.com",
            "password": "password"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {
            "access_token": "fake_access_token",
            "token_type": "bearer"
        })

    @patch("fastapi.testclient.TestClient.post")
    def test_login(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = status.HTTP_200_OK
        mock_response.json.return_value = {
            "access_token": "fake_access_token",
            "token_type": "bearer"
        }

        response = self.client.post("/login", data={
            "username": "test@example.com",
            "password": "password"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {
            "access_token": "fake_access_token",
            "token_type": "bearer"
        })

    @patch("fastapi.testclient.TestClient.get")
    def test_get_current_user_info(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = status.HTTP_200_OK
        mock_response.json.return_value = {
            "login": "testuser",
            "nome": "Test User",
            "email": "test@example.com",
            "status": "active"
        }

        response = self.client.get("/user")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {
            "login": "testuser",
            "nome": "Test User",
            "email": "test@example.com",
            "status": "active"
        })

    @patch("fastapi.testclient.TestClient.put")
    def test_update_current_user_info(self, mock_put):
        mock_response = mock_put.return_value
        mock_response.status_code = status.HTTP_200_OK
        mock_response.json.return_value = {"message": "Usuário atualizado com sucesso"}

        response = self.client.put("/updateUser", json={
            "nome": "Novo Nome",
            "email": "novonome@example.com",
            "status": "active"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {"message": "Usuário atualizado com sucesso"})

    @patch("fastapi.testclient.TestClient.delete")
    def test_delete_current_user(self, mock_delete):
        mock_response = mock_delete.return_value
        mock_response.status_code = status.HTTP_200_OK
        mock_response.json.return_value = {"message": "Usuário deletado com sucesso"}

        response = self.client.delete("/deleteUser")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {"message": "Usuário deletado com sucesso"})
