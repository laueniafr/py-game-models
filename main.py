import json

from pathlib import Path
from db.models import Race, Skill, Player, Guild
from django.utils import timezone


def main() -> None:
    json_path = Path("players.json")

    # Lê o conteúdo do arquivo
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    for nickname, player_data in data.items():
        email = player_data["email"]
        bio = player_data["bio"]

        # === RACE ===
        race_info = player_data["race"]
        race_name = race_info["name"]
        race_description = race_info["description"]

        # Cria ou recupera a Race
        race_obj, _ = Race.objects.get_or_create(
            name=race_name,
            defaults={"description": race_description}
        )

        # === SKILLS ===
        for skill in race_info["skills"]:
            skill_name = skill["name"]
            skill_bonus = skill["bonus"]

            # Cria ou recupera a Skill com base no nome e raça
            Skill.objects.get_or_create(
                name=skill_name,
                race=race_obj,
                defaults={"bonus": skill_bonus}
            )

        # === GUILD ===
        guild_data = player_data.get("guild")
        guild_obj = None

        if guild_data:
            guild_name = guild_data["name"]
            guild_description = guild_data["description"]

            guild_obj, _ = Guild.objects.get_or_create(
                name=guild_name,
                defaults={"description": guild_description}
            )

        # === PLAYER ===
        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": email,
                "bio": bio,
                "race": race_obj,
                "guild": guild_obj,
                "created_at": timezone.now()
            }
        )


if __name__ == "__main__":
    main()
