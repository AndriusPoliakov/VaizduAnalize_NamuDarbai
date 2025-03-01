import { useState } from "react";
import { Button } from "./components/Button";

export default function UploadPage() {
    const [image, setImage] = useState(null);
    const [video, setVideo] = useState(null);
    const [preview, setPreview] = useState(null);
    const [videoPreview, setVideoPreview] = useState(null);

    const handleImageUpload = async (e) => {
        const file = e.target.files[0];
        setImage(file);
    };

    const handleVideoUpload = async (e) => {
        const file = e.target.files[0];
        setVideo(file);
    };

    const submitImage = async () => {
        if (!image) return;
        const formData = new FormData();
        formData.append("file", image);

        const response = await fetch("http://localhost:5000/upload/image", {
            method: "POST",
            body: formData,
        });
        const blob = await response.blob();
        setPreview(URL.createObjectURL(blob));
    };

    const submitVideo = async () => {
        if (!video) return;
        const formData = new FormData();
        formData.append("file", video);

        const response = await fetch("http://localhost:5000/upload/video", {
            method: "POST",
            body: formData,
        });
        const blob = await response.blob();
        setVideoPreview(URL.createObjectURL(blob));
    };

    return (
        <div className="p-6 space-y-4">
            <h1 className="text-xl font-bold">Vaizdo analizės įrankis</h1>
            
            <div className="space-y-2">
                <label className="block font-medium">Įkelti nuotrauką</label>
                <input type="file" accept="image/*" onChange={handleImageUpload} />
                <Button onClick={submitImage} disabled={!image}>Analizuoti</Button>
            </div>
            {preview && <img src={preview} alt="Processed" className="mt-4 w-96 rounded" />}

            <div className="space-y-2">
                <label className="block font-medium">Įkelti vaizdo įrašą</label>
                <input type="file" accept="video/*" onChange={handleVideoUpload} />
                <Button onClick={submitVideo} disabled={!video}>Sekti droną</Button>
            </div>
            {videoPreview && <video controls className="mt-4 w-96 rounded"><source src={videoPreview} type="video/mp4" /></video>}
        </div>
    );
}
