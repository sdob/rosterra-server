from rest_framework.views import APIView
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer

class ObtainAuthToken(APIView):

    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        """
        Take a request containing a token and, if it's valid,
        return a token and user primary key in JSON format.
        This allows us to send an individual requesting user's data
        back to them, and doesn't expose anything that an attacker with
        access to the token wouldn't be able to get anyway.
        """
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': user.pk})
    
obtain_auth_token = ObtainAuthToken.as_view()
