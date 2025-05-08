import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .config import Settings
from .routers import home, health, chat, login, user, project, document
from .utils import init_root_project_dir


def setup_logging(config: Settings):
    logging_level = getattr(logging, config.logging.level.upper())
    logging.basicConfig(
        level=logging_level,
        format=config.logging.format,
        filename=config.logging.filename
    )

def create_app() -> FastAPI:
    config = Settings.get_settings()
    BASE_PATH = config.app.base_path

    @asynccontextmanager  
    async def lifespan(app: FastAPI):  
        # Startup 
        setup_logging(config)
        logging.info(f"Starting chat application in {config.app.env} environment")
        logging.info(f"API prefix: {config.app.api_prefix}")
        logging.info(f"Enabled components: {config.app.components}")
        yield  
        # Shutdown  
        logging.info("Shutting down and byebye...") 
    
    app = FastAPI(
        title="GPT-DTSKUL",
        description="API for chat application",
        version="1.0.0",
        debug=config.app.debug,
        docs_url=config.app.docs_url,
        openapi_url=f"{config.app.api_prefix}/openapi.json",
        lifespan=lifespan
    )


    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Change this in production to restrict domains
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(home.router)
    app.include_router(login.router)
    app.include_router(user.router)
    app.include_router(project.router)
    app.include_router(document.router)
    app.include_router(chat.router, prefix=config.app.api_prefix)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    init_root_project_dir()
    config = Settings.get_settings()
    
    uvicorn.run(
        app="app.main:app",
        host=config.app.host,
        port=config.app.port,
        reload=True if config.app.env == "dev" else False,
        log_level=config.logging.level.lower(),
        # ssl_keyfile=config.database.ssl_key_file,
        # ssl_certfile=config.database.ssl_cert_file
    )