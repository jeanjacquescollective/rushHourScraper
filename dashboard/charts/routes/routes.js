import express from 'express';
import controller from '../controllers/Home.js';
import { getCrowds } from '../controllers/api/crowd.js';
const router = express.Router();

router.get('/', controller.home);
router.get("/api/crowds", getCrowds);


export default router;