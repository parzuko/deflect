import Image, { StaticImageData } from "next/image";

interface DemoImageProps {
  src: StaticImageData;
  srcRemoved: StaticImageData;
  alt: string;
}

export function DemoImage({ src, srcRemoved, alt = "Generated using h = 0.3" }: DemoImageProps) {
  return (
    <div className="flex flex-col justify-center items-center md:max-w-fit space-y-2">
      <div className="flex flex-col md:flex-row space-y-3 md:space-y-0  md:space-x-3">
        <Image src={src} alt={alt} width={300} height={300} />
        <Image src={srcRemoved} alt={alt} width={300} height={300} />
      </div>
      <p className="text-center text-sm text-[#64748B]">{alt}</p>
    </div>
  );
}
