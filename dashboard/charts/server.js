import express from 'express';
import bodyParser from 'body-parser'; 
import routes from './routes/routes.js';
import { getCrowds } from './controllers/api/crowd.js';
const app = express();
const port = 3000;

app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static('public'))
app.use('/', routes);


app.listen(port, () => {
    console.log(`Success! Your application is running on port ${port}.`);
  });

