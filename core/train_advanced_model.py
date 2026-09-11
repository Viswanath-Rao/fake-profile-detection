import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def generate_synthetic_dataset(n_samples=5000, random_state=42):
    """
    Generates a realistic distribution of authentic accounts vs fake/bot/clone accounts
    grounded in empirical social network research (e.g. Cresci et al., MIB dataset patterns).
    """
    np.random.seed(random_state)
    n_real = n_samples // 2
    n_fake = n_samples - n_real

    # --- REAL PROFILES (Authentic Users, Creators, Businesses) ---
    real_followers = np.clip(np.random.lognormal(mean=6.0, sigma=1.5, size=n_real), 5, 2_000_000).astype(int)
    real_following = np.clip(np.random.lognormal(mean=5.5, sigma=1.0, size=n_real), 5, 5_000).astype(int)
    real_posts = np.clip(np.random.lognormal(mean=4.0, sigma=1.3, size=n_real), 1, 10_000).astype(int)
    
    real_uname_len = np.random.randint(5, 16, size=n_real)
    real_uname_digits = np.random.binomial(n=4, p=0.15, size=n_real)
    real_uname_digits = np.minimum(real_uname_digits, real_uname_len - 1)
    real_digit_ratio = real_uname_digits / real_uname_len
    
    real_has_bio = np.random.choice([1, 0], p=[0.88, 0.12], size=n_real)
    real_bio_len = real_has_bio * np.random.randint(15, 150, size=n_real)
    
    real_has_pic = np.random.choice([1, 0], p=[0.98, 0.02], size=n_real)
    real_face_count = np.where(real_has_pic == 0, -1, np.random.choice([1, 2, 0], p=[0.78, 0.15, 0.07], size=n_real))
    real_face_ratio = np.where(real_face_count >= 1, np.random.uniform(0.08, 0.45, size=n_real), 0.0)
    real_is_private = np.random.choice([1, 0], p=[0.45, 0.55], size=n_real)
    real_has_url = np.random.choice([1, 0], p=[0.25, 0.75], size=n_real)

    # --- FAKE PROFILES (Spambots, Follower Farms, Scrapers, Clones) ---
    fake_subtypes = np.random.choice(['spambot', 'zombie', 'clone', 'scraper'], size=n_fake, p=[0.40, 0.25, 0.15, 0.20])
    
    fake_followers = np.zeros(n_fake, dtype=int)
    fake_following = np.zeros(n_fake, dtype=int)
    fake_posts = np.zeros(n_fake, dtype=int)
    fake_uname_len = np.zeros(n_fake, dtype=int)
    fake_uname_digits = np.zeros(n_fake, dtype=int)
    fake_has_bio = np.zeros(n_fake, dtype=int)
    fake_bio_len = np.zeros(n_fake, dtype=int)
    fake_has_pic = np.zeros(n_fake, dtype=int)
    fake_face_count = np.zeros(n_fake, dtype=int)
    fake_face_ratio = np.zeros(n_fake, dtype=float)
    fake_is_private = np.zeros(n_fake, dtype=int)
    fake_has_url = np.zeros(n_fake, dtype=int)

    for i, stype in enumerate(fake_subtypes):
        if stype == 'spambot':
            fake_followers[i] = np.random.randint(0, 120)
            fake_following[i] = np.random.randint(600, 7500)
            fake_posts[i] = np.random.randint(0, 4)
            fake_uname_len[i] = np.random.randint(10, 24)
            fake_uname_digits[i] = np.random.randint(4, fake_uname_len[i] - 2)
            fake_has_bio[i] = np.random.choice([0, 1], p=[0.6, 0.4])
            fake_bio_len[i] = fake_has_bio[i] * np.random.randint(5, 50)
            fake_has_pic[i] = np.random.choice([0, 1], p=[0.4, 0.6])
            fake_face_count[i] = -1 if fake_has_pic[i] == 0 else np.random.choice([0, 2], p=[0.7, 0.3])
            fake_face_ratio[i] = 0.0 if fake_face_count[i] <= 0 else np.random.uniform(0.01, 0.06)
            fake_is_private[i] = 0
            fake_has_url[i] = np.random.choice([1, 0], p=[0.7, 0.3])
        elif stype == 'zombie':
            fake_followers[i] = np.random.randint(500, 20000)
            fake_following[i] = np.random.randint(0, 30)
            fake_posts[i] = np.random.randint(0, 2)
            fake_uname_len[i] = np.random.randint(8, 18)
            fake_uname_digits[i] = np.random.randint(2, 8)
            fake_has_bio[i] = 0
            fake_bio_len[i] = 0
            fake_has_pic[i] = np.random.choice([0, 1], p=[0.7, 0.3])
            fake_face_count[i] = -1 if fake_has_pic[i] == 0 else 0
            fake_face_ratio[i] = 0.0
            fake_is_private[i] = 0
            fake_has_url[i] = 0
        elif stype == 'clone':
            fake_followers[i] = np.random.randint(20, 500)
            fake_following[i] = np.random.randint(150, 800)
            fake_posts[i] = np.random.randint(1, 8)
            fake_uname_len[i] = np.random.randint(12, 22)
            fake_uname_digits[i] = np.random.randint(1, 5)
            fake_has_bio[i] = 1
            fake_bio_len[i] = np.random.randint(20, 90)
            fake_has_pic[i] = 1
            fake_face_count[i] = np.random.choice([1, 0], p=[0.5, 0.5])
            fake_face_ratio[i] = np.random.uniform(0.02, 0.12) if fake_face_count[i] == 1 else 0.0
            fake_is_private[i] = 0
            fake_has_url[i] = 1
        else: # scraper
            fake_followers[i] = np.random.randint(0, 15)
            fake_following[i] = np.random.randint(100, 3000)
            fake_posts[i] = 0
            fake_uname_len[i] = np.random.randint(10, 20)
            fake_uname_digits[i] = np.random.randint(5, 12)
            fake_has_bio[i] = 0
            fake_bio_len[i] = 0
            fake_has_pic[i] = 0
            fake_face_count[i] = -1
            fake_face_ratio[i] = 0.0
            fake_is_private[i] = 0
            fake_has_url[i] = 0

    fake_digit_ratio = fake_uname_digits / np.maximum(fake_uname_len, 1)

    followers = np.concatenate([real_followers, fake_followers])
    following = np.concatenate([real_following, fake_following])
    posts = np.concatenate([real_posts, fake_posts])
    uname_len = np.concatenate([real_uname_len, fake_uname_len])
    uname_digits = np.concatenate([real_uname_digits, fake_uname_digits])
    digit_ratio = np.concatenate([real_digit_ratio, fake_digit_ratio])
    has_bio = np.concatenate([real_has_bio, fake_has_bio])
    bio_len = np.concatenate([real_bio_len, fake_bio_len])
    has_pic = np.concatenate([real_has_pic, fake_has_pic])
    face_count = np.concatenate([real_face_count, fake_face_count])
    face_ratio = np.concatenate([real_face_ratio, fake_face_ratio])
    is_private = np.concatenate([real_is_private, fake_is_private])
    has_url = np.concatenate([real_has_url, fake_has_url])

    y = np.array([0] * n_real + [1] * n_fake)

    ff_ratio = followers / (following + 1.0)
    activity_density = posts / (np.log10(followers + following + 10.0))

    df = pd.DataFrame({
        'followers': followers,
        'following': following,
        'posts': posts,
        'ff_ratio': ff_ratio,
        'activity_density': activity_density,
        'username_length': uname_len,
        'username_digits': uname_digits,
        'digit_ratio': digit_ratio,
        'has_bio': has_bio,
        'bio_length': bio_len,
        'has_profile_pic': has_pic,
        'face_count': face_count,
        'face_ratio': face_ratio,
        'is_private': is_private,
        'has_external_url': has_url,
        'fake': y
    })

    return df

def train_and_export():
    print("Generating comprehensive realistic profile dataset (6,000 samples)...")
    df = generate_synthetic_dataset(n_samples=6000, random_state=42)

    features = [
        'followers', 'following', 'posts', 'ff_ratio', 'activity_density',
        'username_length', 'username_digits', 'digit_ratio',
        'has_bio', 'bio_length', 'has_profile_pic', 'face_count',
        'face_ratio', 'is_private', 'has_external_url'
    ]

    X = df[features]
    y = df['fake']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print(f"Training ensemble model on {len(X_train)} samples across {len(features)} engineered features...")
    
    rf = RandomForestClassifier(n_estimators=150, max_depth=12, min_samples_split=4, random_state=42)
    gb = GradientBoostingClassifier(n_estimators=120, learning_rate=0.08, max_depth=5, random_state=42)
    ensemble = VotingClassifier(estimators=[('rf', rf), ('gb', gb)], voting='soft')
    
    ensemble.fit(X_train, y_train)

    preds = ensemble.predict(X_test)
    probs = ensemble.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds)
    rec = recall_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    auc = roc_auc_score(y_test, probs)

    print("\n--- MODEL PERFORMANCE METRICS ---")
    print(f"Accuracy : {acc * 100:.2f}%")
    print(f"Precision: {prec * 100:.2f}%")
    print(f"Recall   : {rec * 100:.2f}%")
    print(f"F1-Score : {f1 * 100:.2f}%")
    print(f"ROC-AUC  : {auc:.4f}")
    print("---------------------------------")

    os.makedirs('core', exist_ok=True)
    advanced_bundle = {
        'model': ensemble,
        'feature_names': features,
        'metrics': {
            'accuracy': float(acc),
            'precision': float(prec),
            'recall': float(rec),
            'f1': float(f1),
            'auc': float(auc)
        }
    }
    
    with open('core/advanced_model.pkl', 'wb') as f:
        pickle.dump(advanced_bundle, f)
    print("Saved core/advanced_model.pkl")

    X_legacy = df[['followers', 'following', 'posts', 'ff_ratio']]
    X_tr_l, X_te_l, y_tr_l, y_te_l = train_test_split(X_legacy, y, test_size=0.2, random_state=42)
    rf_legacy = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf_legacy.fit(X_tr_l, y_tr_l)
    with open('model.pkl', 'wb') as f:
        pickle.dump(rf_legacy, f)
    print("Updated root model.pkl with robust 4-feature trained model")

if __name__ == '__main__':
    train_and_export()
