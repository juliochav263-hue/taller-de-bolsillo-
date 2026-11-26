const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
const files=['dist/muestras/caja-de-feria.html','herramientas/caja-de-feria/kit/caja-de-feria.html'];
for(const file of files){
 const script=fs.readFileSync(file,'utf8').match(/<script>([\s\S]+)<\/script>/)[1];
 new vm.Script(script);
 const a=script.indexOf('function puedeVender'),b=script.indexOf('function nuevaFeria');
 const r=script.indexOf('function resumen'),e=script.indexOf('function el');
 const backup=script.indexOf('function respaldoValido'),end=script.indexOf("document.querySelector('#restore').addEventListener");
 const ctx=vm.createContext({});vm.runInContext(script.slice(a,b)+script.slice(r,e)+script.slice(backup,end),ctx);
 for(let stock=0;stock<80;stock++)for(let sold=0;sold<=stock;sold++)for(let qty=1;qty<=20;qty++)
   assert.equal(ctx.puedeVender(stock,sold,qty),sold+qty<=stock);
 assert.equal(ctx.puedeVender(undefined,3,200),true);
 for(const qty of [0,-1,1.5,10001,NaN])assert.equal(ctx.puedeVender(undefined,0,qty),false);
 const summary=ctx.resumen({ventas:[{medio:'qr',precio:1000,costo:400,cant:3},{medio:'efectivo',precio:900,costo:500,cant:2}],qr:10,puesto:500,viaje:100,otros:0});
 assert.equal(summary.total,4800);assert.equal(summary.n,5);assert.equal(summary.comision,300);assert.equal(summary.limpio,1700);
 const caja=ctx.resumen({ventas:[{medio:'efectivo',precio:1600.25,costo:500,cant:2}],fondo:500,retiros:700,contado:3000.50,puesto:700});
 assert.equal(caja.esperado,3000.50);assert.equal(caja.diferencia,0);assert.equal(caja.limpio,1500.50);
 const retirada=ctx.resumen({ventas:[],fondo:0,retiros:500,contado:0});assert.equal(retirada.esperado,-500);assert.equal(retirada.diferencia,500);
 assert.equal(ctx.resumen({ventas:[],fondo:500,contado:null}).diferencia,null);

 const d={productos:[{id:'a',nombre:'Alfajor',precio:1000,costo:400}],ferias:[{id:'b',ventas:[{nombre:'Alfajor',precio:1000,costo:400,cant:2,medio:'qr'}],llevo:{a:3},qr:10}],actual:'b'};
 assert.equal(ctx.respaldoValido(d),true);assert.equal(ctx.respaldoValido({...d,actual:'x'}),false);
 const bad=structuredClone(d);bad.ferias[0].ventas[0].cant=-1;assert.equal(ctx.respaldoValido(bad),false);
 assert.match(script,/cantidad:cantidad|cant:cantidad/);
}
console.log('129.600 combinaciones de stock entre las dos variantes, cantidades, balance y recuperación aprobados.');

