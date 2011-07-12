from celery.task import task
from celery.task.sets import subtask

from rest_api.models import Url
from rest_api.backend import Request

#TODO: read long_url from memcache
#TODO: ensure with retry that if we made a resquest we have to save the result 
#TODO: should we ensure that user are logged and have permission here two?


class UrlAlreadyUpdatedError(Exception):
    pass


@task(ignore_result=True)
def url_short(url_id):
    logger = url_short.get_logger()
    logger.info("Url shortner to url_id: %s" % url_id)
    url_request.delay(url_id, callback=subtask(url_update))


@task(ignore_result=True)
def url_request(url_id, callback):
    logger = url_request.get_logger()

    url = Url.objects.get(pk=url_id)
    logger.info("Requesting short url to: %s" % url)

    # request an url shortner for the given url
    short_url = Request().create(url.long_url)
    logger.info("Got response: %s" % short_url)

    # spawn a task to update url on db
    subtask(callback).delay(url_id, short_url)


@task(ignore_result=True)
def url_update(url_id, short_url):
    logger = url_update.get_logger()
    url = Url.objects.get(pk=url_id)
    
    # check we already update this url
    if url.key:
        msg = 'Url %s already updated, possible duplicate task!' % url
        raise UrlAlreadyUpdatedError(msg)

    url.key = short_url
    url.save()

    logger.info("Url %s updated with sucess!" % url)
