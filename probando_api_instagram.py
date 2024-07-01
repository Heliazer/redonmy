from instagram_private_api import Client, ClientError

# Datos de autenticación (debes reemplazarlos con tus propios datos)
username = 'tu_usuario'
password = 'tu_contraseña'

def handle_checkpoint(api, challenge_url):
    # Obtener la elección de método de verificación (SMS, email, etc.)
    choices = api.challenge_get(challenge_url)
    if 'step_data' in choices and 'choice' in choices['step_data']:
        for idx, method in enumerate(choices['step_data']['choice']):
            print(f"{idx}: {method}")
        choice = int(input(f"Selecciona un método de verificación (0-{len(choices['step_data']['choice']) - 1}): "))
        api.challenge_select_verify_method(challenge_url, choice)

    # Enviar código de verificación
    code = input("Introduce el código de verificación recibido: ")
    result = api.challenge_send_security_code(challenge_url, code)
    if result.get('status') == 'ok':
        return True
    else:
        return False

# Iniciar sesión en Instagram
try:
    api = Client(username, password)
except ClientError as e:
    if 'checkpoint_challenge_required' in str(e):
        challenge_url = e.error_response.get('challenge', {}).get('url')
        if challenge_url:
            success = handle_checkpoint(api, challenge_url)
            if success:
                print("Verificación completada con éxito.")
            else:
                print("Error al completar la verificación.")
        else:
            print("No se pudo obtener la URL del desafío.")
    else:
        print(f"No se pudo iniciar sesión: {e}")
        exit()

# El resto del código para obtener seguidores/seguidos solo se ejecuta si la autenticación fue exitosa
try:
    user_info = api.authenticated_user_info()
    user_id = user_info['pk']

    # Obtener lista de usuarios que sigues
    following = api.user_following(user_id)
    following_users = [user['username'] for user in following['users']]

    # Obtener lista de usuarios que te siguen
    followers = api.user_followers(user_id)
    followers_users = [user['username'] for user in followers['users']]

    # Mostrar resultados
    print(f"Usuarios que sigues: {', '.join(following_users)}")
    print(f"Usuarios que te siguen: {', '.join(followers_users)}")
except ClientError as e:
    print(f"Error al obtener información: {e}")
