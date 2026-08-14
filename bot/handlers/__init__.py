from aiogram import Router

def setup_routers() -> Router:
    from .start import router as start_router
    from .about import router as about_router
    from .social import router as social_router
    from .faq import router as faq_router
    from .news import router as news_router
    from .contact import router as contact_router
    from .admin import router as admin_router
    from .errors import router as errors_router
    
    router = Router()
    router.include_routers(
        admin_router,
        start_router,
        about_router,
        social_router,
        faq_router,
        news_router,
        contact_router,
        errors_router
    )
    return router
