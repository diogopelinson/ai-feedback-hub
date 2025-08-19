import json
import os
import boto3
from openai import OpenAI

# Inicializa o cliente do Secrets Manager
secrets_client = boto3.client('secretsmanager')

def get_secret(secret_name):
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in response:
            return json.loads(response['SecretString'])
        else:
            return response['SecretBinary']
    except Exception as e:
        print(f"Erro ao buscar o secret: {e}")
        raise e

OPENAI_SECRET_NAME = os.environ.get('OPENAI_SECRET_NAME', 'openai-api-key-feedback-hub')

secrets = get_secret(OPENAI_SECRET_NAME)
openai_api_key = secrets.get('OPENAI_API_KEY')

client = OpenAI(api_key=openai_api_key)

def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'OPTIONS,POST'
    }

    # Lida com requisições OPTIONS para CORS preflight
    if event.get('httpMethod' ) == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'CORS preflight success'})
        }

    try:
        body = json.loads(event['body'])
        user_text = body.get('text', '')

        if not user_text:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'O campo "text" é obrigatório.'})
            }

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um avaliador de textos em português. Forneça feedback detalhado, incluindo pontos positivos, sugestões de melhoria e uma nota geral de 0 a 10 para clareza, gramática e coesão."},
                {"role": "user", "content": f"Avalie o texto abaixo e dê feedback detalhado:\n{user_text}"}
            ],
            max_tokens=500, # Aumentado para feedback mais detalhado
            temperature=0.7 # Ajustado para respostas mais equilibradas
        )

        feedback = response.choices[0].message.content

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'feedback': feedback})
        }

    except Exception as e:
        print(f"Erro na execução da Lambda: {e}")
        return {
            'statusCode': 500,
            'headers': headers, # Inclui headers CORS mesmo em caso de erro
            'body': json.dumps({'error': str(e)})
        }
