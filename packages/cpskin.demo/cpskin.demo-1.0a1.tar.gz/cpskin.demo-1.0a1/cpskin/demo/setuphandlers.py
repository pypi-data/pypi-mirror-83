# -*- coding: utf-8 -*-
from plone.app.event.interfaces import IEventSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import datetime
import os

from imio.helpers.content import create, richtextval, add_image


def post_install(context):
    """Post install script."""
    if context.readDataFile('cpskindemo_default.txt') is None:
        return

    portal = context.getSite()
    # frontpage = api.content.get('/front-page')
    # frontpage.processForm()
    # Edit frontpage to have explain text on how use demo site
    add_events(portal)
    add_news(portal)
    add_folders(portal)
    add_album(portal)
    add_users(portal)


def add_events(portal):
    """Add some demo events."""
    timezone = 'Europe/Brussels'
    reg = getUtility(IRegistry)
    settings = reg.forInterface(IEventSettings, prefix="plone.app.event")
    if not settings.portal_timezone:
        settings.portal_timezone = timezone
    now = datetime.datetime.now()
    tomorrow = datetime.datetime(now.year, now.month, now.day + 1)
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    events = [
        {
            'cont': '/evenements', 'type': 'Event',
            'title': 'Atelier photo',
            'attrs': {'description': 'Participer à un atelier photo',
                      'start': datetime.datetime(now.year, now.month, now.day, 18),
                      'end': datetime.datetime(now.year, now.month, now.day, 21),
                      'timezone': timezone,
                      'hiddenTags': set([u'a-la-une', ])},
            'functions': [add_image],
            'extra': {'add_image': {'filepath': os.path.join(data_path, 'atelierphoto.jpg')}},
            'trans': ['publish_and_hide'],
        },
        {
            'cont': '/evenements', 'type': 'Event',
            'title': 'Concert',
            'attrs': {'description': 'Participer à notre concert caritatif',
                      'start': datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 21),
                      'end': datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23),
                      'timezone': timezone},
            'functions': [add_image],
            'extra': {'add_image': {'filepath': os.path.join(data_path, 'concert.jpg')}},
            'trans': ['publish_and_hide'],
        },
        {
            'cont': '/evenements', 'type': 'Event',
            'title': 'Marché aux fleurs',
            'attrs': {'description': 'Vener découvrir notre marché aux fleurs',
                      'start': tomorrow,
                      'end': tomorrow + datetime.timedelta(weeks=1),
                      'timezone': timezone},
            'functions': [add_image],
            'extra': {'add_image': {'filepath': os.path.join(data_path, 'marcheauxfleurs.jpg')}},
            'trans': ['publish_and_hide'],
        },
    ]
    create(events)


def add_news(portal):
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    news = [
        {
            'cont': '/actualites', 'type': 'News Item',
            'title': 'Nouvelle brasserie',
            'attrs': {'description': 'Une nouvelle brasserie va ouvrir ses portes près de chez vous',
                      'text': richtextval('Bonjour, <br /><br />Une nouvelle brasserie va ouvrir ses portes près de '
                                          'chez vous'),
                      'hiddenTags': set([u'a-la-une', ])},
            'functions': [add_image],
            'extra': {'add_image': {'filepath': os.path.join(data_path, 'brasserie.jpg')}},
            'trans': ['publish_and_hide'],
        },
        {
            'cont': '/actualites', 'type': 'News Item',
            'title': 'Météo',
            'attrs': {'description': 'Attention à la météo de ces prochains jours',
                      'text': richtextval('Bonjour, <br /><br />Faites attention à la météo de ces prochains jours'),},
            'functions': [add_image],
            'extra': {'add_image': {'filepath': os.path.join(data_path, 'meteo.jpg')}},
            'trans': ['publish_and_hide'],
        },
    ]
    create(news)


def add_folders(portal):

    folders = [
        {
            'cid': 100, 'cont': '/ma-commune', 'type': 'Folder',
            'title': u'Vie politique',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 110, 'cont': 100, 'type': 'Folder',
            'title': u'Collège communal',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 111, 'cont': 100, 'type': 'Folder',
            'title': u'Conseil communal',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 200, 'cont': '/ma-commune', 'type': 'Folder',
            'title': u'Services communaux',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 210, 'cont': 200, 'type': 'Folder',
            'title': u'Population-Etat civil',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 220, 'cont': 200, 'type': 'Folder',
            'title': u'Informatique',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 230, 'cont': 200, 'type': 'Folder',
            'title': u"Heures d'ouverture",
            'trans': ['publish_and_hide'],
        },
        {
            'cid': 240, 'cont': 200, 'type': 'Folder',
            'title': u'Autres services',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 250, 'cont': 240, 'type': 'Folder',
            'title': u'CPAS',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 260, 'cont': 250, 'type': 'Folder',
            'title': u'Album photos',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 300, 'cont': '/loisirs', 'type': 'Folder',
            'title': u'Sports',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 310, 'cont': 300, 'type': 'Folder',
            'title': u'Piscine communale',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 320, 'cont': 300, 'type': 'Folder',
            'title': u'Annuaire des clubs sportifs',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 400, 'cont': '/loisirs', 'type': 'Folder',
            'title': u'Folklores',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 410, 'cont': 400, 'type': 'Folder',
            'title': u'Carnaval',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 420, 'cont': 400, 'type': 'Folder',
            'title': u'Marché de Noël',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 500, 'cont': '/loisirs', 'type': 'Folder',
            'title': u'Tourisme',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 510, 'cont': 500, 'type': 'Folder',
            'title': u'Barrage',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 600, 'cont': '/economie', 'type': 'Folder',
            'title': u"L'entreprenariat",
            'trans': ['publish_and_show'],
        },
        {
            'cid': 610, 'cont': 600, 'type': 'Folder',
            'title': u'CSAM',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 620, 'cont': 600, 'type': 'Folder',
            'title': u'EId',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 700, 'cont': '/economie', 'type': 'Folder',
            'title': u'Zonings',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 710, 'cont': 700, 'type': 'Folder',
            'title': u'Industriels',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 720, 'cont': 700, 'type': 'Folder',
            'title': u'Port',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 800, 'cont': '/je-suis', 'type': 'Folder',
            'title': u'Jeune',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 810, 'cont': '/je-suis', 'type': 'Folder',
            'title': u'Entrepreneur',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 820, 'cont': '/je-suis', 'type': 'Folder',
            'title': u'Nouvel habitant',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 900, 'cont': '/je-trouve', 'type': 'Folder',
            'title': u'Démarches administratives',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 910, 'cont': '/je-trouve', 'type': 'Folder',
            'title': u'Taxes',
            'trans': ['publish_and_show'],
        },
    ]

    create(folders)


def add_album(portal):
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    objects = [
        {
            'cid': 10,
            'cont': '/', 'type': 'Folder',
            'title': 'Album',
            'trans': ['publish_and_hide'],
        },
        {
            'cid': 15,
            'cont': 10, 'type': 'Image',
            'title': 'Moto',
            'functions': [add_image],
            'extra': {'add_image': {'filepath': os.path.join(data_path, 'moto.jpg')}},
            'trans': ['publish_and_hide'],
        },
        {
            'cid': 20,
            'cont': 10, 'type': 'Image',
            'title': 'Météo',
            'functions': [add_image],
            'extra': {'add_image': {'filepath': os.path.join(data_path, 'meteo.jpg')}},
            'trans': ['publish_and_hide'],
        },
    ]
    cids = create(objects)
    cids[10].setLayout('galleryview')


def add_users(portal):
    pass
