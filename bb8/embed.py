"""
Provides different Discord embed renderings.
"""
from discord import Embed

import re


class CardEmbed:
    """
    Provides base for all card embeds.

    :param card: the card which embed should be rendered for.
    """
    FACTION_COLOURS = {
        "red": int("AC0A1D", 16),
        "blue": int("133278", 16),
        "yellow": int("BD8100", 16),
        "gray": int("979185", 16)
    }

    def __init__(self, card):
        self.card = card
        self.embed = Embed(
            type="rich",
            title=card["label"],
            url=card["url"]
        )

    def colour(self):
        """
        Gets faction colour of card.
        """
        return CardEmbed.FACTION_COLOURS.get(self.card["faction_code"])


class CardImage(CardEmbed):
    """
    Renders embed with full-size image.
    """

    def __init__(self, card):
        super().__init__(card)

    def render(self):
        """
        Renders card image as Discord Embed.
        """
        self.embed.set_image(url=self.card["imagesrc"])
        return self.embed


class CardDetail(CardEmbed):
    """
    Renders embed with card details.
    """

    TEXT_MAPPING = {
        "\[special\]": "swspecial",
        "\[blank\]": "swblank",
        "\[melee\]": "swmelee",
        "\[ranged\]": "swranged",
        "\[indirect\]": "swindirect"
    }

    SIDES_MAPPING = {
        "RD": "swranged",
        "MD": "swmelee",
        "ID": "swindirect",
        "Sh": "swshield",
        "Dr": "swdisrupt",
        "Dc": "swdiscard",
        "F": "swfocus",
        "R": "swresource",
        "Sp": "swspecial",
        "-": "swblank",
    }

    SIDE_PATTERN = re.compile(r'(\+*\d){0,1}([a-zA-Z\-]+)(\d){0,1}')

    def __init__(self, card, emojis):
        super().__init__(card)
        self.text_subs = self._build_substitutions(CardDetail.TEXT_MAPPING,
                                                   emojis)
        self.side_subs = self._build_substitutions(CardDetail.SIDES_MAPPING,
                                                   emojis)

    def type_line(self):
        """
        Construct card's type containing faction, affiliation and rarity
        as well as cost.

        Example:

            Character: Villain - Rogue - Rare • Points: 8/11 • Health: 8
        """
        parts = [self.card["type_name"].title() + ": "]

        character = [
            self.card["affiliation_name"],
            self.card["faction_name"],
            self.card["rarity_name"]
        ]
        parts.append(" - ".join(character))

        lines = {
            "character": ["Points: {points}", "Health: {health}"],
            "support": ["Cost: {cost}"],
            "upgrade": ["Cost: {cost}"],
            "event": ["Cost: {cost}"],
            "battlefield": []
        }

        typ = self.card["type_code"]
        parts.extend((" • " + s).format(**self.card) for s in lines[typ])

        return "".join(parts)

    def text_line(self):
        """
        Constructs card text by substituting icons with emojis and
        adding dice sides iconography.

        Example:

            :special: - Deal 2 Damage to each of an opponent's characters.
            Discard this upgrade from play.

        :return: the card text and dice description
        :rtype: str
        """
        result = self.card["text"] if "text" in self.card else "(no text)"
        for target, sub in self.text_subs.items():
            result = re.sub(target, sub, result)
        result = re.sub(r"<b>(.+)</b>", r"**\1**", result)
        result = re.sub(r"<em>(.+)</em>", r"*\1*", result)
        result = re.sub(r"<i>(.+)</i>", r"*\1*", result)

        if "sides" in self.card:
            dice_line = self._dice_line(self.card["sides"])
            result += f"\n{dice_line}"

        return result

    def _dice_line(self, sides):
        """
        Constructs dice side line by substituting icons with emojis.

        :param list sides: The dice sides to be included
        :return: the visualized all dice sides
        :rtype: str
        """
        parts = [self._side_icon(side) for side in sides]
        return " | ".join(parts) + "\n"

    def _side_icon(self, side):
        """
        Constructs dice side by parsing value, icon and extra cost.

        :param str side: the description of side
        :return: transformed dice sides
        :rtype: str
        """
        match = CardDetail.SIDE_PATTERN.match(side)
        if match:
            value, icon, extra_cost = match.groups()

            for pattern, emoji in self.side_subs.items():
                if re.match(pattern, icon):
                    icon = emoji
                    break

            line = icon
            if value and value == '0':
                line = f"X {line}"
            elif value:
                line = f"{value} {line}"

            if extra_cost:
                resource = self.side_subs["R"]
                line = f"{line} / {extra_cost} {resource}"

            return line

        return None

    def _build_substitutions(self, mapping, emojis):
        """
        Builds emoji substitutions for given mapping.

        :param dict mapping: the mapping of shortcuts to emoji names
        :param list emojis: the list of available emojis
        :return: the mapping of card icons to emoji hashes.
        """
        return {
            pattern: self._find_emoji(name, emojis)
            for pattern, name in mapping.items()
            if self._find_emoji(name, emojis)
        }

    def _find_emoji(self, name, emojis):
        """
        Gets emoji hash for emoji with given name.

        :param str name: the emoji name, e.g. swspecial
        :param list emojis: the list of available emojis
        :return: the emoji hash or None if emoji with given name does not exists
        """
        for emoji in emojis:
            if emoji.name == name:
                return str(emoji)
        return None

    def footer_line(self):
        """
        Constructs footer line containing illustrator,
        set membership and position.

        Example:

            Tony Fotti • Awakenings # 64

        :return: the footer line describing card set and illustrator
        :rtype: str
        """
        parts = []
        if "illustrator" in self.card and self.card["illustrator"].strip():
            parts.append(self.card["illustrator"])
        parts.append(
            "{} #{}".format(self.card["set_name"], self.card["position"])
        )

        return " • ".join(parts)

    def render(self):
        """
        Renders card detail as Discord Embed.

        :return: the rendered embed
        """
        self.embed.add_field(
            name=self.type_line(),
            value=self.text_line()
        )
        self.embed.colour = self.colour()
        self.embed.set_footer(text=self.footer_line())
        self.embed.set_thumbnail(url=self.card["imagesrc"])

        return self.embed
