import { DemoImage } from "@/components/demo-image";
import { Upload } from "@/components/upload";

import building from "@/public/images/building.jpg";
import buildingRemoved from "@/public/images/buildingFix.jpeg";

import dog from "@/public/images/dog.jpg";
import dogRemoved from "@/public/images/dogFix.jpeg";

import train from "@/public/images/train.jpg";
import trainRemoved from "@/public/images/trainFix.jpeg";

export default function Home() {
  const images = [
    {
      original: building,
      fixed: buildingRemoved,
      h: 0.04,
    },
    {
      original: dog,
      fixed: dogRemoved,
      h: 0.03,
    },
    {
      original: train,
      fixed: trainRemoved,
      h: 0.033,
    },
  ];

  return (
    <main className="flex flex-col justify-center items-center py-20">
      <section className="flex flex-col justify-center items-center max-w-4xl">
        <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">Reflection Remover</h1>
        <p className="leading-7 [&:not(:first-child)]:mt-6 text-center">
          This project was built for CS-2364 as the final project submission. It is a code based implementation of{" "}
          <a href="https://arxiv.org/pdf/1903.03889" className="text-cyan-600 hover:text-cyan-500">
            {" "}
            Fast Single Image Reflection Suppression via Convex Optimization
          </a>
          . Upload an image below and try it!
        </p>
        <Upload />
      </section>

      <section className="flex flex-col justify-center max-w-7xl mt-10 px-5">
        <h2 className="scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight first:mt-0">Example Images</h2>
        <p className="leading-7 [&:not(:first-child)]:mt-6">
          Below are a few examples of images from the white paper, depicting synthetically generated reflections on
          images and the corresponding h value which was used to remove them
        </p>
        <div className="flex flex-wrap gap-4 items-start">
          {images.map((image, index) => (
            <DemoImage
              key={index}
              src={image.original}
              srcRemoved={image.fixed}
              alt={`Generated using h = ${image.h} `}
            />
          ))}
        </div>
      </section>
    </main>
  );
}
