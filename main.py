import uvicorn

from api.review import app
from config import appConfig

if __name__ == '__main__':
    print('start.......jj....')
    uvicorn.run(app, debug=True, port=int(appConfig.PORT), host='0.0.0.0')
