import Svg, { Circle, Path, Text as SvgText } from 'react-native-svg';

/** Moeda do PyPasso (dourada com o "Py"). */
export function Moeda({ size = 22 }: { size?: number }) {
  return (
    <Svg width={size} height={size} viewBox="0 0 24 24">
      <Circle cx="12" cy="12.8" r="10" fill="#C98A12" />
      <Circle cx="12" cy="11.6" r="10" fill="#FFC83D" />
      <Circle cx="12" cy="11.6" r="7.2" fill="none" stroke="#E0A21C" strokeWidth="1.4" />
      <SvgText x="12" y="15.3" textAnchor="middle" fontSize="9.5" fontWeight="900" fill="#9A6408">Py</SvgText>
      <Path d="M6.5 7.5a7 7 0 0 1 4-2.4" stroke="#FFF2C2" strokeWidth="1.5" strokeLinecap="round" fill="none" />
    </Svg>
  );
}
