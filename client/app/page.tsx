import { Upload } from "@/components/upload";
import Image from "next/image";

export default function Home() {
  return (
    <main className="flex flex-col justify-center items-center py-20">
      <div className="flex flex-col justify-center items-center max-w-4xl">
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
      </div>
    </main>
  );
}
