// Server-side boundary for a future Stripe/session integration. Never trusts URL flags or localStorage.
export default async function handler(request) {
 const headers={'Content-Type':'application/json','Cache-Control':'no-store'};
 if(request.method!=='POST')return new Response(JSON.stringify({error:'method_not_allowed'}),{status:405,headers:{...headers,Allow:'POST'}});
 let body;try{body=await request.json()}catch{return new Response(JSON.stringify({error:'invalid_request'}),{status:400,headers})}
 if(body.productId!=='personal-ai-operations-director-v2')return new Response(JSON.stringify({error:'unknown_product'}),{status:404,headers});
 if(body.action==='checkout')return new Response(JSON.stringify({error:'checkout_not_configured'}),{status:503,headers});
 // TODO: verify signed server session, then look up a webhook-created entitlement.
 // Do not unlock hub content or downloads until both a session and entitlement are verified.
 return new Response(JSON.stringify({access:'not_purchased',error:'verified_entitlement_required'}),{status:403,headers});
}
