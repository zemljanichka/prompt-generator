import os
import gettext
from typing import Callable

def setup_i18n(lang: str) -> Callable:
    """
    Set up internationalization for the given language.
    
    Args:
        lang: Language code ('en' or 'ru')
        
    Returns:
        gettext.gettext: Translation function
    """
    # Define the path to the locale directory
    localedir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locale')
    
    # Set up translations
    try:
        translation = gettext.translation('messages', localedir=localedir, languages=[lang])
        translation.install()
        return translation.gettext
    except FileNotFoundError:
        # Fallback to default English if translation file not found
        return gettext.gettext 