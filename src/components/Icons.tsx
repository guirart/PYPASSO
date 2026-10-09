import Svg, { Path } from 'react-native-svg';

type P = { size?: number; color: string };
const mk = (d: string, stroke = false) => ({ size = 22, color }: P) => (
  <Svg width={size} height={size} viewBox="0 0 24 24">
    <Path d={d} fill={stroke ? 'none' : color} stroke={stroke ? color : 'none'} strokeWidth={stroke ? 3 : 0} strokeLinecap="round" strokeLinejoin="round" />
  </Svg>
);

export const Flame = mk('M12 2c1 3.5-1.5 5-1.5 7.5 0 1.4 1 2.5 2.3 2.5 1.6 0 2.4-1.4 2.2-3.5C17.6 10.6 19 13 19 15.5 19 19.6 15.9 22 12 22s-7-2.4-7-6.5C5 10 11 7.5 12 2z');
export const Bolt = mk('M13 2 4 14h7l-1 8 9-12h-7z');
export const Heart = mk('M12 21s-7.5-4.6-9.6-9.3C1 8.4 3.2 4.5 7 4.5c2.1 0 3.6 1.2 5 3 1.4-1.8 2.9-3 5-3 3.8 0 6 3.9 4.6 7.2C19.5 16.4 12 21 12 21z');
export const Star = mk('m12 2.5 2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z');
export const Lock = mk('M7 10V8a5 5 0 0 1 10 0v2h1a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1v-9a1 1 0 0 1 1-1zm2 0h6V8a3 3 0 0 0-6 0z');
export const Trophy = mk('M7 3h10v2h3v3a4 4 0 0 1-4 4h-.3A5 5 0 0 1 13 14.9V18h3v3H8v-3h3v-3.1A5 5 0 0 1 8.3 12H8a4 4 0 0 1-4-4V5h3zm0 4H6v1a2 2 0 0 0 1.2 1.8A5 5 0 0 1 7 8zm10 0v1q0 .9-.2 1.8A2 2 0 0 0 18 8V7z');
export const Check = mk('m4.5 12.5 5 5 10-11', true);
export const Cross = mk('M6.5 6.5l11 11M17.5 6.5l-11 11', true);
export const Path_ = mk('M5 4h6a3 3 0 0 1 0 6H9a3 3 0 0 0 0 6h10', true);
export const Person = mk('M12 12a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9zm-8 9c0-4 3.6-7 8-7s8 3 8 7z');
export const CodeIcon = mk('M8 7 3 12l5 5M16 7l5 5-5 5M13.5 5l-3 14', true);
export const Dumbbell = mk('M6.5 7v10M17.5 7v10M3.5 9.5v5M20.5 9.5v5M6.5 12h11', true);
export const Book = mk('M4 5.5C4 4.7 4.7 4 5.5 4H11v15H5.5A1.5 1.5 0 0 1 4 17.5zM20 5.5c0-.8-.7-1.5-1.5-1.5H13v15h5.5c.8 0 1.5-.7 1.5-1.5z');
export const Target = mk('M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zm0 4a5 5 0 1 1 0 10 5 5 0 0 1 0-10zm0 3.2a1.8 1.8 0 1 0 0 3.6 1.8 1.8 0 0 0 0-3.6z');
export const Flag = mk('M6 21V4M6 4h11l-2.5 4L17 12H6', true);
