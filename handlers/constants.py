from handlers import autoreg, trends_parser, community_parser, subscribers_parser

handlers = {
    "Autoreg": autoreg.start,
    "Trends Parser": trends_parser.start,
    "Community Parser": community_parser.start,
    "Subscribers Parser": subscribers_parser.start,
}
