# -*- coding: utf-8 -*-
import urllib2
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from cpskin.cirkwi import _


class CirkwiView(BrowserView):
    index = ViewPageTemplateFile("cirkwiview.pt")

    def render(self):
        return self.index()

    def cdf_parametres(self):
        # String sample for "comblain-au-pont" : "cdf_id_host:3249,cdf_id_outil:570,cdf_lang:fr"
        cdf_host = "cdf_id_host:" + self.context.cdf_host
        cdf_outils = "cdf_id_outils:" + self.context.cdf_outils
        if self.context.cdf_lang is None:
            # no language was set in cirkwi object so we use Plone instance language.
            self.context.cdf_lang = self.context.language
        cdf_lang = "cdf_lang:" + self.context.cdf_lang
        return "%s,%s,%s" % (cdf_host, cdf_outils, cdf_lang)

    def __call__(self):
        return self.render()

    def getpage(self, cdf_parametres_client='', em_name=''):
        cdf_page_url = 'http://outil.cirkwi.com/outil/client_recherche_page_client.php'
        cdf_file_url = 'http://outil.cirkwi.com/outil/client_recherche_fichier_client.php'
        try:
            qs = self.request.form
            if 'type' not in qs:  # we must get a page
                cdf_url = "%s?%s" % (cdf_page_url, qs)
                if 'cdf_parametres_client' not in qs:
                    cdf_url = "%s&cdf_parametres_client=%s" % (cdf_url, cdf_parametres_client)
            else:  # we must get a file
                cdf_url = "%s?%s" % (cdf_file_url, qs)
                if qs['type'] == 'xml':
                    self.request.response.setHeader('content-type', 'text/xml')
                elif qs['type'] == 'texte':
                    self.request.response.setHeader('content-type', 'text/html')
                elif qs['type'] == 'image':
                    self.request.response.setHeader('content-type', 'text/jpeg')
            conn = urllib2.urlopen(cdf_url)
            data = conn.read()
            conn.close()
            data = data.replace('href="page_membre.php?',
                                'target="_blank" href="http://www.circuits-de-belgique.be/page_membre.php?')
            data = data.replace('href="page.php?',
                                'target="_blank" href="http://www.circuits-de-belgique.be/page.php?')
            if data == '2':
                error = _(u"Look at your host id!")
                raise Exception(error)
            # patch for a good escape sequence in data document.writer(... <\/script>") code.
            data = data.replace("</script\\>\")", "<\/script>\")")            
            return data
        except Exception, msg:
            return _(u"Cannot open url '%s': %s" % (cdf_url, msg))
