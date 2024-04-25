use serde::{Deserialize, Serialize};
use gloo_utils::format::json::JsValueSerdeExt;  // Ensure gloo_utils is included in Cargo.toml
use wasm_bindgen::prelude::*;
use wasm_bindgen_futures::JsFuture;
use web_sys::{Request, RequestInit, RequestMode, Response};
use yew::prelude::*;

#[derive(Serialize, Deserialize)]
struct ChatRequest {
    prompt: String,
}

#[derive(Serialize, Deserialize)]
struct ChatResponse {
    response: String,
}

#[function_component(App)]
fn app() -> Html {
    let input = use_state(|| String::new());
    let response = use_state(|| String::new());

    let oninput = {
        let input = input.clone();
        Callback::from(move |e: InputEvent| {
            let input_value = e.target_unchecked_into::<web_sys::HtmlInputElement>().value();
            input.set(input_value);
        })
    };

    let onsubmit = {
        let input = input.clone();
        let response = response.clone(); // Clone for use inside the closure
        Callback::from(move |_| {
            let response = response.clone(); // Further clone for async block
            let prompt = (*input).clone();
            wasm_bindgen_futures::spawn_local(async move {
                let result = send_prompt(&prompt).await;
                response.set(result);
            });
        })
    };

    html! {
        <>
            <h1>{"Chat with AI"}</h1>
            <input {oninput} value={(*input).clone()} />
            <button {onsubmit}>{"Send"}</button>
            <p>{(*response).clone()}</p>
        </>
    }
}

async fn send_prompt(prompt: &str) -> String {
    let chat_request = ChatRequest {
        prompt: prompt.to_string(),
    };

    let mut opts = RequestInit::new();
    opts.method("POST");
    opts.mode(RequestMode::Cors);
    let request_body = serde_json::to_string(&chat_request).unwrap();
    opts.body(Some(&JsValue::from_str(&request_body)));

    let request = Request::new_with_str_and_init("/api/chat", &opts).unwrap();

    let window = web_sys::window().unwrap();
    let response_val = JsFuture::from(window.fetch_with_request(&request)).await;

    if let Ok(resp) = response_val {
        let resp: Response = resp.dyn_into().unwrap();
        if resp.ok() {
            let json = JsFuture::from(resp.json().unwrap()).await.unwrap();
            if let Ok(res_text) = json.into_serde::<ChatResponse>() {
                return res_text.response;
            }
        }
    }

    "Failed to get response".to_string()
}

#[wasm_bindgen(start)]
pub fn run_app() {
    yew::start_app::<App>();
}
