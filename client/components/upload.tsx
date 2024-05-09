"use client";

import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useState } from "react";

import hiddenImage from "@/public/no-image.svg";

type CardProps = React.ComponentProps<typeof Card>;

export function Upload({ className, ...props }: CardProps) {
  const [imageString, setImageString] = useState<string | null>(null);
  const [imageLoaded, setImageLoaded] = useState<boolean>(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const formData = new FormData(form);

    const hValue = formData.get("h") as string;
    const picture = formData.get("file");

    if (!hValue || !picture) {
      alert("Please fill in the form!");
      return;
    }

    if (Number(hValue) < 0 || Number(hValue) > 1) {
      alert("Please enter a valid threshold value between 0 and 1");
      return;
    }

    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    if (res.ok) {
      const data = await res.json();
      setImageString(data.image);
      setImageLoaded(true);
    } else {
      alert("An error occurred while uploading the image");
    }
  };

  return (
    <div className="flex items-center md:flex-row flex-col md:space-x-10">
      <Card className="w-[350px] my-10">
        <CardHeader>
          <CardTitle>Upload Image</CardTitle>
          <CardDescription>Set the params and remove reflections!</CardDescription>
        </CardHeader>
        <CardContent>
          <form id="uploadForm" onSubmit={handleSubmit}>
            <div className="grid w-full items-center gap-4">
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="h">H Value</Label>
                <Input id="h" name="h" placeholder="Enter a threshold value between 0 and 1" />
              </div>
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="file">Picture</Label>
                <Input id="file" name="file" type="file" />
              </div>
            </div>
          </form>
        </CardContent>
        <CardFooter>
          <Button form="uploadForm" type="submit" className="w-full">
            ✨ Remove Reflections
          </Button>
        </CardFooter>
      </Card>
      <Image
        src={!imageLoaded ? hiddenImage : `data:image/jpeg;base64, ${imageString}`}
        alt="image"
        width={300}
        height={300}
      />
    </div>
  );
}
