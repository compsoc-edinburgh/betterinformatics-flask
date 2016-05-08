from betterinformatics import BI
from betterinformatics import app

bi = BI(app, config_path="config.yml")
bi.gen_views()

bi.run()
