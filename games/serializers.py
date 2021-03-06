from rest_framework import serializers
from games.models import GameCategory
from games.models import Game
from games.models import Player
from games.models import PlayerScore

class GameCategorySerializer(serializers.HyperlinkedModelSerializer):
    games = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='game-detail'
    )
    
    class Meta:
        model = GameCategory
        fields = (
            'url',
            'pk',
            'name',
            'games'
        )

class GameSerializer(serializers.HyperlinkedModelSerializer):
    # we want to display the game category's name instead of the id
    game_category = serializers.SlugRelatedField(
        queryset=GameCategory.objects.all(),
        slug_field='name') 
    
    class Meta:
        model = Game
        fields = (
            'url',
            'game_category',
            'name',
            'release_date',
            'played'
        )
    
class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    # we want to display all the details for the game
    game = GameSerializer()
    #we dont include the player coz it will be nested in the player
    class Meta:
        model = PlayerScore
        fields = (
            'url',
            'pk',
            'score',
            'score_date',
            'game'
        )

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    scores = ScoreSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(
        choices=Player.GENDER_CHOICES
    )
    gender_description = serializers.CharField(
        source='get_gender_display',
        read_only=True
    )
    
    class Meta:
        model = Player
        fields = (
            'url',
            'name',
            'gender',
            'gender_description',
            'scores'
        )

class PlayerScoreSerializer(serializers.HyperlinkedModelSerializer):
    player = serializers.SlugRelatedField(queryset=Player.objects.all(), slug_field='name')
    # we want to display the game's name instead of the id
    game  = serializers.SlugRelatedField(queryset=Game.objects.all(), slug_field='name')

    class Meta:
        model = PlayerScore
        fields = (
            'url',
            'pk',
            'score',
            'score_date',
            'player',
            'game'
        )



# class GameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Game
#         fields = ('id',
#         'name',
#         'release_date',
#         'game_category',
#         'played')

# class GameSerializer(serializers.Serializer):
#     pk = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=200)
#     release_date = serializers.DateTimeField()
#     game_category = serializers.CharField(max_length=200)
#     played = serializers.BooleanField(required=False)

#     def create(self, validated_data):
#         return Game.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.release_date = validated_data('release_date', instance.release_date)
#         instance.game_category = validated_data('game_category', instance.game_category)
#         instance.played = validated_data.get('played', instance.played)
#         instance.save()
#         return instance

