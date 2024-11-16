// import express from 'express';
// import cors from 'cors';
// import { exec } from 'child_process';

// const app = express();
// const PORT = process.env.PORT || 5000;

// app.use(cors());  // Enable CORS

// app.get('/download', async (req, res) => {
//   const videoUrl = req.query.url;

//   if (!videoUrl) {
//     return res.status(400).send('No URL provided');
//   }

//   console.log(`Requesting download for video: ${videoUrl}`);

//   try {
//     // Set headers for the download response
//     res.header('Content-Disposition', 'attachment; filename="video.mp4"');
//     res.header('Content-Type', 'video/mp4');

//     // Full path to yt-dlp.exe on your Desktop
//     const ytDlpPath = "C:\\Users\\DELL\\Desktop\\yt-dlp.exe";
    
//     // Command without specific format to let yt-dlp pick the best available
//     const command = `"${ytDlpPath}" -o - ${videoUrl} --verbose`;

//     // Start the yt-dlp process to download the video
//     const downloadProcess = exec(command);

//     // Pipe the yt-dlp output (video stream) to the client
//     downloadProcess.stdout.pipe(res);

//     // Log the standard output and error logs
//     downloadProcess.stdout.on('data', (data) => {
//       console.log('yt-dlp stdout:', data.toString());
//     });

//     downloadProcess.stderr.on('data', (data) => {
//       console.error('yt-dlp stderr output:', data.toString());
//     });

//     // Listen for process exit (yt-dlp finishing)
//     downloadProcess.on('close', (code) => {
//       if (code !== 0) {
//         console.error(`yt-dlp process exited with code ${code}`);
//         if (!res.headersSent) { // Check if headers were already sent
//           res.status(500).send('yt-dlp exited with error code.');
//         }
//       }
//     });

//   } catch (error) {
//     // Handle unexpected errors
//     console.error('Error downloading video:', error);
//     if (!res.headersSent) { // Check if headers were already sent
//       res.status(500).send('Failed to download the video');
//     }
//   }
// });

// app.listen(PORT, () => {
//   console.log(`Backend server running on http://localhost:${PORT}`);
// });
