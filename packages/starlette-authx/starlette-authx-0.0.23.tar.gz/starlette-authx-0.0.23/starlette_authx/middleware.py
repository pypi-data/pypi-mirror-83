from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Scope, Receive, Send
import asyncio
from . import ipaccess, basic, bearer, utils, InvalidToken, oauth2_cookie


class AuthXMiddleware:
    _AUTH_METHODS = {
        'oauth2_cookie': oauth2_cookie,
        'ipaccess': ipaccess,
        'bearer': bearer,
        'basic': basic,
    }
    # TODO: from config/modifiable
    _known_paths = {
        '/docs': 'has_any_auth()',
        '/redoc': 'has_any_auth()',
        '/openapi.json': 'has_any_auth()',
        '/graphql': 'has_any_auth()'
    }

    def __init__(self, app: ASGIApp, config: dict) -> None:
        self._app = app
        self._config = config
        self._validate_config()

    # TODO: validate all config - not just bearer
    def _validate_config(self):
        """
        this stuff is mostly from https://gitlab.com/jorgecarleitao/starlette-oauth2-api
        """
        if 'bearer' in self._config:
            providers = self._config.get('bearer').get('providers')
            mandatory_keys = {'issuer', 'keys', 'audience'}
            for provider in providers:
                if not mandatory_keys.issubset(set(providers[provider])):
                    raise ValueError(
                        f'Each provider must contain the following keys: {mandatory_keys}. Provider "{provider}" is missing {mandatory_keys - set(providers[provider])}.')

                keys = providers[provider]['keys']
                if isinstance(keys, str) and keys.startswith('http://'):
                    raise ValueError(
                        f'When "keys" is a url, it must start with "https://". This is not true in the provider "{provider}"')

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            for method in self._AUTH_METHODS.keys():
                if method in self._config:
                    _config = self._config[method]
                    result = await self._AUTH_METHODS[method].process(_config, scope, receive, send)
                    if asyncio.iscoroutine(result):
                        return await result

            # check current request for general auth actions
            if scope['path'] in self._known_paths.keys():
                if not utils.validator(condition=self._known_paths[scope['path']], config=scope.get('authx', {})):
                    response = JSONResponse({'message': 'unauthorized'}, status_code=401)
                    await response(scope, receive, send)
            else:
                await self._app(scope, receive, send)

        except InvalidToken as e:
            response = JSONResponse({'message': str(e)}, status_code=401)
            await response(scope, receive, send)
