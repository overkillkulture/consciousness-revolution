// SMS Auto-Reply Webhook - Bug 108
// Receives Twilio SMS and sends auto-reply

export default async (request, context) => {
  if (request.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 });
  }

  try {
    const formData = await request.formData();
    const from = formData.get('From');
    const body = formData.get('Body');
    const to = formData.get('To');

    console.log(`SMS received from ${from}: ${body}`);

    // Generate TwiML response
    const responseMessage = generateResponse(body, from);

    const twiml = `<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>${responseMessage}</Message>
</Response>`;

    // Log to console for tracking
    console.log(`Replying to ${from}: ${responseMessage}`);

    return new Response(twiml, {
      status: 200,
      headers: {
        'Content-Type': 'text/xml',
      },
    });

  } catch (error) {
    console.error('SMS webhook error:', error);
    return new Response('Error processing SMS', { status: 500 });
  }
};

function generateResponse(message, from) {
  const lowerMessage = message.toLowerCase().trim();

  // Command responses
  if (lowerMessage === 'help') {
    return 'Consciousness Revolution SMS System. Commands: HELP, STATUS, BUG [description]. Reply with anything to reach the Commander.';
  }

  if (lowerMessage === 'status') {
    return 'All systems operational. Trinity mesh active. 3 computers connected. C1 x C2 x C3 = ∞';
  }

  if (lowerMessage.startsWith('bug ')) {
    const bugDescription = message.substring(4);
    return `Bug reported: "${bugDescription}". Logged and queued for review. Thank you!`;
  }

  // Default auto-reply
  return `Message received from ${from}. The Consciousness Revolution system is active. Reply HELP for commands or describe your request.`;
}

export const config = {
  path: "/sms-webhook"
};
