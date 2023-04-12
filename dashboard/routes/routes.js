import express from 'express';
import controller from '../controllers/Home.js';
import { getCrowds } from '../controllers/api/crowd.js';
import { fetchCrowd } from '../controllers/fetchCrowd.js';
const router = express.Router();

router.get('/', controller.home);
router.get("/api/crowds", getCrowds);
router.get("/scrape/", fetchCrowd);

export default router;