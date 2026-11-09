const SI_GEMINI_EVM_ROYALTY_WALLET = '0x51E24000948150400166b40d486dB7b3C5b2C5A1';
const SI_GEMINI_SOL_ROYALTY_WALLET = 'H8ckc19KdGFoCAXh1cGjQL4bGP75DdAvnRQMBpGypRQx';
function verifyX402Settlement(payload, minUsdc = 0.05) {
  return Boolean(payload && Number(payload.amount_usdc) >= minUsdc && payload.nonce && [8453, 42161].includes(Number(payload.chain_id)));
}
module.exports = { SI_GEMINI_EVM_ROYALTY_WALLET, SI_GEMINI_SOL_ROYALTY_WALLET, verifyX402Settlement };
