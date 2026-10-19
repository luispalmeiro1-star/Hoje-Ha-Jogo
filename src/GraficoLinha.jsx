// Os gráficos de linha da app vivem num ficheiro à parte para o recharts — a
// biblioteca mais pesada da app — só ser descarregado quando alguém abre um
// ecrã com gráfico, e não logo à entrada, onde atrasava o primeiro ecrã de
// toda a gente.
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const ESTILO_TOOLTIP = {background:"#14160f",border:"1px solid #23271b",borderRadius:8,color:"white",fontSize:11};

// destacarMeu: o ponto da própria pessoa (payload.isMe) aparece maior e branco.
export default function GraficoLinha({data,altura,eixoX,valor,cor,corEixo="#8a9080",rotulo,sufixo="",inteiros=false,destacarMeu=false}) {
  const ponto = destacarMeu
    ? ({cx,cy,payload})=><circle key={payload[eixoX]} cx={cx} cy={cy} r={payload.isMe?5:3} fill={payload.isMe?"#ffffff":cor} stroke="none"/>
    : {fill:cor,r:3};
  return (
    <ResponsiveContainer width="100%" height={altura}>
      <LineChart data={data} margin={{top:5,right:10,left:-20,bottom:5}}>
        <XAxis dataKey={eixoX} tick={{fill:corEixo,fontSize:10}} tickLine={false} axisLine={false}/>
        <YAxis tick={{fill:corEixo,fontSize:10}} tickLine={false} axisLine={false} allowDecimals={!inteiros}/>
        <Tooltip contentStyle={ESTILO_TOOLTIP} formatter={(v)=>[`${v}${sufixo}`,rotulo]} cursor={{stroke:"#23271b"}}/>
        <Line type="monotone" dataKey={valor} stroke={cor} strokeWidth={2} dot={ponto} activeDot={destacarMeu?{r:5,fill:"#ffffff"}:{r:5}}/>
      </LineChart>
    </ResponsiveContainer>
  );
}
