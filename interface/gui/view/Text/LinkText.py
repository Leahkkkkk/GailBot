from dataclasses import dataclass

from view.Text.WelcomePageText import WelcomePageText

dataclass
class Links: 
        _linkTemplate = "<a href={0}>{1}</a>"
        
        tutorialLink = _linkTemplate.format("https://sites.tufts.edu/hilab", WelcomePageText.tutorialText)
        
        guideLink = _linkTemplate.format('https://sites.tufts.edu/hilab', WelcomePageText.guideText)

        gbWebLink = _linkTemplate.format("https://sites.tufts.edu/hilab", WelcomePageText.gbLinkText)
        
        gbWebLink = _linkTemplate.format("https://sites.tufts.edu/hilab", WelcomePageText.guideText)
        