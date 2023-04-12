import * as path from 'path';
import * as fs from 'fs';
export default {
    home: (req, res) => {   
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
        res.setHeader('Access-Control-Allow-Credentials', true);  
        res.sendFile(path.join(path.resolve(path.dirname('')), 'public/index.html'));
    },
};